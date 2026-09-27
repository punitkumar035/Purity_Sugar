"""
solver/stations/heat_exchanger.py
Purity for Sugar — Heat Exchanger Station Model

Rules:
  - Two fluid sides: Process fluid (cold side) and Heating medium (hot side)
  - If port1_required or target outlet temp specified, calculates required heating fluid flow (RULES_v5.md §A7)
  - Heating steam condenses to saturated liquid with optional condensate_drop_k subcooling
  - Crystals in heated process stream dissolve if stream becomes undersaturated (RULES_v5.md §A9)
  - Heat balance: Q_cold = Q_hot * (1 - heat_loss)
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream
from engine.fluids import water_sat_temp_c, water_enthalpy_kJkg
from engine.crystals import crystals_forward


class HeatExchangerStation(BaseStation):
    def calculate(
        self,
        inlet_streams: Dict[str, Stream],
        inlet_flow_ids: List[str],
        outlet_flow_ids: List[str],
        atmospheric_p_kpa: float = 101.325,
    ) -> StationResult:
        warnings = []
        required_inlets = {}

        if not inlet_flow_ids:
            return StationResult(
                outlet_streams={ofid: Stream() for ofid in outlet_flow_ids},
                warnings=["Heat exchanger has no inlet flows."],
            )

        # Port 0 = process stream, Port 1 = heating stream
        proc_in_id = inlet_flow_ids[0]
        proc_in = inlet_streams.get(proc_in_id, Stream()).copy()

        heat_in_id = inlet_flow_ids[1] if len(inlet_flow_ids) > 1 else None
        heat_in = inlet_streams.get(heat_in_id, Stream()).copy() if heat_in_id else None

        t_out_spec = self.get_float("temperature_out_c", -999.0)
        t_rise_spec = self.get_float("temperature_rise_k", -999.0)
        approach = self.get_float("approach_c", -999.0)
        cond_drop = self.get_float("condensate_drop_k", 0.0)
        heat_loss_pct = self.get_float("heat_loss_pct", 0.0)
        heat_eff = max(0.01, 1.0 - heat_loss_pct / 100.0)
        port1_req = self.get_bool("port1_required", False)

        # Determine target process outlet temperature
        t_target = proc_in.temperature_c
        if t_out_spec > -200.0:
            t_target = t_out_spec
        elif t_rise_spec > -200.0:
            t_target = proc_in.temperature_c + t_rise_spec
        elif approach > -200.0 and heat_in:
            t_target = heat_in.temperature_c - approach

        t_proc_out = max(proc_in.temperature_c, t_target)

        # Specific heat of process stream
        # Q_cold = m_proc * (h_out - h_in)
        proc_out_temp_stream = proc_in.copy()
        proc_out_temp_stream.temperature_c = t_proc_out
        delta_h_proc = proc_out_temp_stream.enthalpy_kjkg - proc_in.enthalpy_kjkg
        q_duty_kjh = proc_in.mass_flow_kgh * max(0.0, delta_h_proc)

        # Heating side duty: Q_hot = Q_duty / heat_eff
        q_hot_req_kjh = q_duty_kjh / heat_eff

        m_heat_actual = heat_in.mass_flow_kgh if heat_in else 0.0
        t_heat_out = 20.0
        p_heat_out = heat_in.pressure_kpa if heat_in else atmospheric_p_kpa

        if heat_in:
            # Check if heating stream is steam
            is_steam = heat_in.gas_pct > 50.0
            if is_steam:
                # Steam condenses
                t_sat = water_sat_temp_c(heat_in.pressure_kpa)
                t_cond = max(0.0, t_sat - cond_drop)
                h_steam_in = heat_in.enthalpy_kjkg
                h_cond_out = water_enthalpy_kJkg(t_cond, heat_in.pressure_kpa, quality=0.0)
                latent_kjkg = max(50.0, h_steam_in - h_cond_out)

                if port1_req or (t_out_spec > -200.0 or t_rise_spec > -200.0):
                    # Calculate required steam mass flow
                    req_steam = q_hot_req_kjh / latent_kjkg
                    required_inlets[heat_in_id] = req_steam
                    m_heat_actual = req_steam

                t_heat_out = t_cond
            else:
                # Sensible liquid heating (e.g. hot juice or condensate)
                # m_heat * cp * (t_in - t_out) = Q_hot
                # Assume cp ~ 4.0 kJ/kg K
                cp_heat = 4.0
                if port1_req and t_target > -200.0:
                    delta_t_hot = max(5.0, heat_in.temperature_c - proc_in.temperature_c - 5.0)
                    req_heat_flow = q_hot_req_kjh / (cp_heat * delta_t_hot)
                    required_inlets[heat_in_id] = req_heat_flow
                    m_heat_actual = req_heat_flow
                    t_heat_out = heat_in.temperature_c - delta_t_hot
                elif m_heat_actual > 0.0:
                    delta_t_hot = q_hot_req_kjh / (m_heat_actual * cp_heat)
                    t_heat_out = max(proc_in.temperature_c, heat_in.temperature_c - delta_t_hot)

        # 1. Process stream output
        proc_out = proc_in.copy()
        proc_out.temperature_c = t_proc_out

        # Crystal dissolution check upon heating (RULES_v5.md §A9)
        if proc_out.crystal_fraction > 1e-5:
            ss = proc_out.supersaturation
            if ss < 0.9999 and proc_out.water > 1e-5:
                try:
                    res = crystals_forward(
                        ds_mc=proc_out.ds_fraction,
                        pu_mc=proc_out.purity_fraction,
                        temp_c=proc_out.temperature_c,
                        ss=1.0,
                        a=proc_out.sol_coef_a,
                        b=proc_out.sol_coef_b,
                        c=proc_out.sol_coef_c,
                    )
                    new_cryst = max(0.0, res["crystal_frac"])
                    diss = max(0.0, proc_out.crystal_fraction - new_cryst)
                    proc_out.sucrose_crystals = new_cryst
                    proc_out.dissolved_sucrose += diss
                    proc_out.normalize()
                except Exception:
                    pass

        # 2. Heating stream output
        if heat_in:
            heat_out = heat_in.copy()
            heat_out.mass_flow_kgh = m_heat_actual
            heat_out.temperature_c = t_heat_out
            if heat_in.gas_pct > 50.0:
                # Phase change: saturated steam -> liquid condensate
                heat_out.water = 1.0
                heat_out.water_vapor = 0.0
                heat_out.normalize()
        else:
            heat_out = Stream(mass_flow_kgh=0.0, temperature_c=20.0, pressure_kpa=atmospheric_p_kpa)

        outlet_streams = {}
        if len(outlet_flow_ids) == 1:
            outlet_streams[outlet_flow_ids[0]] = proc_out
        elif len(outlet_flow_ids) >= 2:
            outlet_streams[outlet_flow_ids[0]] = proc_out
            outlet_streams[outlet_flow_ids[1]] = heat_out
            for ofid in outlet_flow_ids[2:]:
                outlet_streams[ofid] = Stream(mass_flow_kgh=0.0, temperature_c=20.0, pressure_kpa=atmospheric_p_kpa)

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "heat_duty_kw": round(q_duty_kjh / 3600.0, 2),
                "process_temp_out_c": round(t_proc_out, 2),
                "heating_temp_out_c": round(t_heat_out, 2),
                "heating_flow_kgh": round(m_heat_actual, 2),
            },
            warnings=warnings,
            required_inlet_flows=required_inlets,
        )
