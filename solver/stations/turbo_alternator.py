"""
solver/stations/turbo_alternator.py
Purity for Sugar — Turbo Alternator (Turbogenerator) Station Model

Rules:
  - Steam turbine driving an electric generator
  - If elec_power_output_kw > 0, steam inlet is a REQUIRED FLOW (RULES_v5.md §A7)
  - Electrical Power = Mechanical Power * eta_electrical
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream
from engine.fluids import water_sat_temp_c, water_enthalpy_kJkg


class TurboAlternatorStation(BaseStation):
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
                warnings=["Turbo alternator has no inlet flows."],
            )

        steam_id = inlet_flow_ids[0]
        steam_in = inlet_streams.get(steam_id, Stream()).copy()

        p_disch = self.get_float("pressure_out_kpa", 150.0)
        p_drop = self.get_float("pressure_drop_kpa", -1.0)
        if p_drop > 0.0:
            p_disch = max(10.0, steam_in.pressure_kpa - p_drop)

        eta_isentropic = self.get_float("isentropic_eff_pct", 75.0) / 100.0
        eta_mech = self.get_float("mechanical_eff_pct", 96.0) / 100.0
        eta_elec = self.get_float("electrical_eff_pct", 95.0) / 100.0
        elec_power_spec_kw = self.get_float("elec_power_output_kw", -1.0)

        t_sat_in = water_sat_temp_c(steam_in.pressure_kpa)
        t_sat_out = water_sat_temp_c(p_disch)
        delta_h_isentropic = max(50.0, 4.2 * (t_sat_in - t_sat_out) * 2.2)
        delta_h_actual = delta_h_isentropic * eta_isentropic

        total_eta = eta_mech * eta_elec

        m_steam = steam_in.mass_flow_kgh
        if elec_power_spec_kw > 0.0:
            req_flow = (elec_power_spec_kw * 3600.0) / (delta_h_actual * total_eta)
            required_inlets[steam_id] = req_flow
            m_steam = req_flow

        elec_power_generated_kw = (m_steam / 3600.0) * delta_h_actual * total_eta

        exhaust = steam_in.copy()
        exhaust.mass_flow_kgh = m_steam
        exhaust.pressure_kpa = p_disch
        exhaust.temperature_c = max(t_sat_out, steam_in.temperature_c - (t_sat_in - t_sat_out))

        outlet_streams = {}
        if outlet_flow_ids:
            n_out = len(outlet_flow_ids)
            for ofid in outlet_flow_ids:
                s = exhaust.copy()
                s.mass_flow_kgh = m_steam / n_out
                outlet_streams[ofid] = s

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "inlet_pressure_kpa": steam_in.pressure_kpa,
                "discharge_pressure_kpa": p_disch,
                "steam_flow_kgh": m_steam,
                "electrical_power_kw": round(elec_power_generated_kw, 2),
                "total_efficiency_pct": round(total_eta * 100.0, 1),
            },
            warnings=warnings,
            required_inlet_flows=required_inlets,
        )
