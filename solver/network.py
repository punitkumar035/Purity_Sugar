"""
solver/network.py
Purity for Sugar — Sequential Modular Network Flowsheet Solver
Phase 03

Governed by:
  - RULES_v5.md §A4 (Station Numbering & Calculation Sequence)
  - RULES_v5.md §A7 (Required Flows Backward Propagation)
  - RULES_v5.md §A8 (Pressure Rules & Propagation)
  - RULES_v5.md §A12 (JSON Contract: Schema v1.0, HTTP 200 for all solver outcomes)
  - RULES_v5.md §C1 (Convergence Tolerance: default 0.01% / 0.0001, Max Iterations: 150)
  - RULES_v5.md §C2 (Fatal Errors vs Non-Fatal Warnings)
"""

from __future__ import annotations
import math
from typing import Dict, Any, List, Optional, Tuple, Set

from solver.stream import Stream
from solver.schemas import (
    SolveRequest,
    SolveResponse,
    StationOutput,
    FlowOutput,
    StationInput,
    FlowInput,
    RevenuesSummary,
    FlowRevenueItem,
)
from solver.stations import create_station, BaseStation, StationResult


class NetworkSolver:
    """Sequential modular flowsheet solver executing station models and converging recycle loops."""

    def __init__(self, request: SolveRequest):
        self.request = request
        self.stations: Dict[str, BaseStation] = {}
        self.station_order: List[BaseStation] = []
        self.flows: Dict[str, FlowInput] = {f.id: f for f in request.flows}
        self.flow_states: Dict[str, Stream] = {}
        self.station_inlets: Dict[str, List[str]] = {}   # station_key -> list of flow_ids
        self.station_outlets: Dict[str, List[str]] = {}  # station_key -> list of flow_ids
        self.recycle_flow_ids: Set[str] = set()          # flow IDs that form feedback/recycle loops
        self.warnings: List[str] = []
        self.errors: List[str] = []
        self.station_results: Dict[str, StationResult] = {}

    def _build_topology(self) -> bool:
        """Parses stations, builds station number execution sequence, and maps flow connections."""
        # 1. Check duplicate station numbers (RULES_v5.md §A4, §C2)
        used_nums: Set[int] = set()
        station_id_map: Dict[str, str] = {}  # maps both id and str(station_number) to station_key

        for st_in in self.request.stations:
            if st_in.station_number in used_nums:
                self.errors.append(f"Fatal: Duplicate station number {st_in.station_number} detected (§A4).")
                return False
            used_nums.add(st_in.station_number)

            st_obj = create_station(
                station_type=st_in.type,
                station_id=st_in.id,
                station_number=st_in.station_number,
                name=st_in.name,
                properties=st_in.properties,
            )
            key = st_in.id
            self.stations[key] = st_obj
            station_id_map[st_in.id] = key
            station_id_map[str(st_in.station_number)] = key
            self.station_inlets[key] = []
            self.station_outlets[key] = []

        # Sequence stations: lower numbers solved first (RULES_v5.md §A4)
        self.station_order = sorted(self.stations.values(), key=lambda s: s.station_number)

        # 2. Map flows to stations and initialize streams
        atm_p = self.request.atmospheric_pressure_kpa or 101.325

        for f in self.request.flows:
            # Initialize flow stream
            st = Stream.from_initial_state(f.initial_state or {}, default_p_kpa=atm_p)
            self.flow_states[f.id] = st

            # Connect origin station
            if f.origin_station is not None and str(f.origin_station).strip() not in ("", "0"):
                orig_key = station_id_map.get(str(f.origin_station).strip())
                if orig_key:
                    self.station_outlets[orig_key].append(f.id)

            # Connect dest station
            if f.dest_station is not None and str(f.dest_station).strip() not in ("", "0"):
                dest_key = station_id_map.get(str(f.dest_station).strip())
                if dest_key:
                    self.station_inlets[dest_key].append(f.id)

            # Detect recycle / feedback streams (origin station solved at or after destination station)
            if f.origin_station is not None and f.dest_station is not None:
                o_key = station_id_map.get(str(f.origin_station).strip())
                d_key = station_id_map.get(str(f.dest_station).strip())
                if o_key and d_key and o_key in self.stations and d_key in self.stations:
                    if self.stations[o_key].station_number >= self.stations[d_key].station_number:
                        self.recycle_flow_ids.add(f.id)

        return True

    def solve(self) -> SolveResponse:
        """Executes sequential modular solving with Wegstein / successive substitution acceleration."""
        if not self._build_topology():
            return SolveResponse(
                status="invalid",
                iterations=0,
                final_error=1.0,
                error_message="; ".join(self.errors),
                stations=[],
                flows=[],
            )

        if not self.stations:
            return SolveResponse(
                status="invalid",
                iterations=0,
                final_error=0.0,
                error_message="No stations found in flowsheet.",
                stations=[],
                flows=[],
            )

        tol = max(1e-6, self.request.convergence_tolerance or 0.0001)
        max_iter = 1 if self.request.single_pass else max(1, self.request.max_iterations or 150)
        atm_p = self.request.atmospheric_pressure_kpa or 101.325

        iteration = 0
        final_err = 0.0
        converged = False

        while iteration < max_iter:
            iteration += 1
            max_delta = 0.0

            # Store prior flow states for convergence tracking
            prior_flows = {fid: s.copy() for fid, s in self.flow_states.items()}

            # 1. Forward sweep: execute stations in ascending station_number order
            for st in self.station_order:
                in_flow_ids = self.station_inlets[st.station_id]
                out_flow_ids = self.station_outlets[st.station_id]

                # Gather inlet streams
                in_streams = {fid: self.flow_states[fid] for fid in in_flow_ids}

                try:
                    res = st.calculate(
                        inlet_streams=in_streams,
                        inlet_flow_ids=in_flow_ids,
                        outlet_flow_ids=out_flow_ids,
                        atmospheric_p_kpa=atm_p,
                    )
                except Exception as ex:
                    return SolveResponse(
                        status="invalid",
                        iterations=iteration,
                        final_error=1.0,
                        error_message=f"Station {st.station_number} ('{st.name}') calculation error: {str(ex)}",
                        stations=self._build_station_outputs(),
                        flows=self._build_flow_outputs(),
                    )

                self.station_results[st.station_id] = res

                # Update outlet flow states
                for ofid, out_st in res.outlet_streams.items():
                    if ofid in self.flow_states:
                        if ofid in self.recycle_flow_ids and iteration > 1:
                            # Apply relaxation on recycle / tear streams to prevent limit cycles
                            alpha = 0.6
                            s_old = prior_flows[ofid]
                            s_rel = out_st.copy()
                            s_rel.mass_flow_kgh = (1.0 - alpha) * s_old.mass_flow_kgh + alpha * out_st.mass_flow_kgh
                            s_rel.water = (1.0 - alpha) * s_old.water + alpha * out_st.water
                            s_rel.dissolved_sucrose = (1.0 - alpha) * s_old.dissolved_sucrose + alpha * out_st.dissolved_sucrose
                            s_rel.non_sucrose_1 = (1.0 - alpha) * s_old.non_sucrose_1 + alpha * out_st.non_sucrose_1
                            s_rel.non_sucrose_2 = (1.0 - alpha) * s_old.non_sucrose_2 + alpha * out_st.non_sucrose_2
                            s_rel.temperature_c = (1.0 - alpha) * s_old.temperature_c + alpha * out_st.temperature_c
                            s_rel.normalize()
                            self.flow_states[ofid] = s_rel
                        else:
                            self.flow_states[ofid] = out_st

                # 2. Backward propagation of required flows (RULES_v5.md §A7)
                if res.required_inlet_flows:
                    for r_fid, req_mass in res.required_inlet_flows.items():
                        if r_fid in self.flow_states:
                            curr_st = self.flow_states[r_fid]
                            curr_st.mass_flow_kgh = req_mass

            # 3. Check convergence on all internal flows
            for fid, s_now in self.flow_states.items():
                s_old = prior_flows[fid]
                # Compare mass flow rate
                denom_m = max(1.0, abs(s_now.mass_flow_kgh))
                rel_err_m = abs(s_now.mass_flow_kgh - s_old.mass_flow_kgh) / denom_m

                # Compare dry substance fraction
                rel_err_ds = abs(s_now.ds_fraction - s_old.ds_fraction)

                # Compare enthalpy
                denom_h = max(100.0, abs(s_now.enthalpy_kjkg))
                rel_err_h = abs(s_now.enthalpy_kjkg - s_old.enthalpy_kjkg) / denom_h

                flow_err = max(rel_err_m, rel_err_ds, rel_err_h)
                if flow_err > max_delta:
                    max_delta = flow_err

            final_err = max_delta

            if max_delta < tol:
                converged = True
                break

        status_str = "converged" if (converged or self.request.single_pass) else "diverged"
        err_msg = ""
        if status_str == "diverged":
            err_msg = f"Balance did not converge within {max_iter} iterations (final relative error: {final_err:.6f}, tolerance: {tol:.6f})."

        # Global mass balance summary and revenues
        balance_summary = self._calculate_global_balance()
        revenues_summary = self._calculate_revenues()
        balance_summary["revenues"] = revenues_summary.model_dump()

        return SolveResponse(
            status=status_str,
            iterations=iteration,
            final_error=round(final_err, 7),
            error_message=err_msg,
            stations=self._build_station_outputs(),
            flows=self._build_flow_outputs(),
            balance_summary=balance_summary,
            revenues=revenues_summary,
        )

    def _calculate_global_balance(self) -> Dict[str, Any]:
        """Calculates global overall mass and dry substance balance closures."""
        total_mass_in = 0.0
        total_mass_out = 0.0
        total_ds_in = 0.0
        total_ds_out = 0.0

        for f in self.request.flows:
            st = self.flow_states.get(f.id)
            if not st:
                continue
            is_feed = f.is_external or f.origin_station is None or str(f.origin_station).strip() in ("", "0")
            is_exit = f.dest_station is None or str(f.dest_station).strip() in ("", "0")

            if is_feed and not is_exit:
                total_mass_in += st.mass_flow_kgh
                total_ds_in += st.mass_flow_kgh * st.ds_fraction
            elif is_exit and not is_feed:
                total_mass_out += st.mass_flow_kgh
                total_ds_out += st.mass_flow_kgh * st.ds_fraction

        mass_diff = abs(total_mass_in - total_mass_out)
        mass_closure_pct = (mass_diff / max(1.0, total_mass_in)) * 100.0

        ds_diff = abs(total_ds_in - total_ds_out)
        ds_closure_pct = (ds_diff / max(1.0, total_ds_in)) * 100.0

        return {
            "total_mass_in_kgh": round(total_mass_in, 2),
            "total_mass_out_kgh": round(total_mass_out, 2),
            "mass_closure_error_pct": round(mass_closure_pct, 4),
            "total_ds_in_kgh": round(total_ds_in, 2),
            "total_ds_out_kgh": round(total_ds_out, 2),
            "ds_closure_error_pct": round(ds_closure_pct, 4),
        }

    def _calculate_revenues(self) -> RevenuesSummary:
        """Calculates process net revenues: (outlet flow revenues) - (inlet flow costs)."""
        curr_sym = self.request.currency_symbol or "$"
        days = max(1.0, float(self.request.campaign_days or 300.0))

        inlet_items: List[FlowRevenueItem] = []
        outlet_items: List[FlowRevenueItem] = []

        tot_c_hr = 0.0
        tot_r_hr = 0.0

        for fid, f in self.flows.items():
            st = self.flow_states.get(fid)
            if not st:
                continue
            is_feed = f.is_external or f.origin_station is None or str(f.origin_station).strip() in ("", "0")
            is_exit = f.dest_station is None or str(f.dest_station).strip() in ("", "0")
            flow_name = f.name or f"Flow {fid}"

            if is_feed and (f.unit_cost or 0.0) > 0:
                u_cost = float(f.unit_cost)
                c_hr = st.mass_flow_kgh * u_cost
                c_day = c_hr * 24.0
                c_camp = c_day * days
                tot_c_hr += c_hr
                inlet_items.append(
                    FlowRevenueItem(
                        id=fid,
                        name=flow_name,
                        mass_flow_kgh=round(st.mass_flow_kgh, 2),
                        unit_price=round(u_cost, 4),
                        rate_per_hour=round(c_hr, 2),
                        rate_per_day=round(c_day, 2),
                        rate_per_campaign=round(c_camp, 2),
                    )
                )

            if is_exit and (f.unit_value or 0.0) > 0:
                u_val = float(f.unit_value)
                r_hr = st.mass_flow_kgh * u_val
                r_day = r_hr * 24.0
                r_camp = r_day * days
                tot_r_hr += r_hr
                outlet_items.append(
                    FlowRevenueItem(
                        id=fid,
                        name=flow_name,
                        mass_flow_kgh=round(st.mass_flow_kgh, 2),
                        unit_price=round(u_val, 4),
                        rate_per_hour=round(r_hr, 2),
                        rate_per_day=round(r_day, 2),
                        rate_per_campaign=round(r_camp, 2),
                    )
                )

        tot_c_day = tot_c_hr * 24.0
        tot_c_camp = tot_c_day * days

        tot_r_day = tot_r_hr * 24.0
        tot_r_camp = tot_r_day * days

        net_hr = tot_r_hr - tot_c_hr
        net_day = tot_r_day - tot_c_day
        net_camp = tot_r_camp - tot_c_camp

        return RevenuesSummary(
            currency_symbol=curr_sym,
            campaign_days=days,
            total_inlet_cost_per_hour=round(tot_c_hr, 2),
            total_inlet_cost_per_day=round(tot_c_day, 2),
            total_inlet_cost_per_campaign=round(tot_c_camp, 2),
            total_outlet_revenue_per_hour=round(tot_r_hr, 2),
            total_outlet_revenue_per_day=round(tot_r_day, 2),
            total_outlet_revenue_per_campaign=round(tot_r_camp, 2),
            net_process_revenue_per_hour=round(net_hr, 2),
            net_process_revenue_per_day=round(net_day, 2),
            net_process_revenue_per_campaign=round(net_camp, 2),
            inlet_flows=inlet_items,
            outlet_flows=outlet_items,
        )

    def _build_station_outputs(self) -> List[StationOutput]:
        res_list = []
        for st in self.station_order:
            calc_props = {}
            st_warnings = []
            if st.station_id in self.station_results:
                sr = self.station_results[st.station_id]
                calc_props = sr.calculated_properties
                st_warnings = sr.warnings

            res_list.append(
                StationOutput(
                    id=st.station_id,
                    station_number=st.station_number,
                    name=st.name,
                    type=st.station_type,
                    calculated_properties=calc_props,
                    warnings=st_warnings,
                )
            )
        return res_list

    def _build_flow_outputs(self) -> List[FlowOutput]:
        res_list = []
        for fid, f in self.flows.items():
            st = self.flow_states.get(fid, Stream())
            wire = st.to_wire_dict(fid)
            wire["name"] = f.name or f"Flow {fid}"
            wire["unit_cost"] = f.unit_cost or 0.0
            wire["unit_value"] = f.unit_value or 0.0

            is_feed = f.is_external or f.origin_station is None or str(f.origin_station).strip() in ("", "0")
            is_exit = f.dest_station is None or str(f.dest_station).strip() in ("", "0")

            c_hr = 0.0
            r_hr = 0.0
            if is_feed and (f.unit_cost or 0.0) > 0:
                c_hr = st.mass_flow_kgh * float(f.unit_cost)
            if is_exit and (f.unit_value or 0.0) > 0:
                r_hr = st.mass_flow_kgh * float(f.unit_value)

            wire["cost_per_hour"] = round(c_hr, 2)
            wire["cost_per_day"] = round(c_hr * 24.0, 2)
            wire["revenue_per_hour"] = round(r_hr, 2)
            wire["revenue_per_day"] = round(r_hr * 24.0, 2)

            res_list.append(FlowOutput(**wire))
        return res_list
