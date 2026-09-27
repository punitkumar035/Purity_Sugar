"""
solver/stations/turbine.py
Purity for Sugar — Steam Turbine Station Model

Rules:
  - Expands high-pressure steam across isentropic expansion
  - If power_output_kw > 0, turbine steam in is a REQUIRED FLOW (RULES_v5.md §A7)
  - Power output: P_kw = m_steam * (h_in - h_out) * eta_mech / 3600
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream, mix_streams
from engine.fluids import water_sat_temp_c, water_enthalpy_kJkg


class TurbineStation(BaseStation):
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
                warnings=["Turbine has no inlet flows."],
            )

        steam_id = inlet_flow_ids[0]
        steam_in = inlet_streams.get(steam_id, Stream()).copy()

        p_disch = self.get_float("discharge_pressure_kpa", 150.0)
        p_drop = self.get_float("pressure_drop_kpa", -1.0)
        if p_drop > 0.0:
            p_disch = max(10.0, steam_in.pressure_kpa - p_drop)

        eta_isentropic = self.get_float("isentropic_eff_pct", 75.0) / 100.0
        eta_mech = self.get_float("mechanical_eff_pct", 95.0) / 100.0
        power_spec_kw = self.get_float("power_output_kw", -1.0)

        # Enthalpy drop across expansion
        h_in = steam_in.enthalpy_kjkg
        # Theoretical isentropic enthalpy drop (approx 200 - 450 kJ/kg for typical sugar mill conditions)
        t_sat_in = water_sat_temp_c(steam_in.pressure_kpa)
        t_sat_out = water_sat_temp_c(p_disch)
        delta_h_isentropic = max(50.0, 4.2 * (t_sat_in - t_sat_out) * 2.2)
        delta_h_actual = delta_h_isentropic * eta_isentropic

        # If power is specified, calculate required steam flow
        m_steam = steam_in.mass_flow_kgh
        if power_spec_kw > 0.0:
            # P_kw = (m_kgh / 3600) * delta_h_actual * eta_mech
            req_flow = (power_spec_kw * 3600.0) / (delta_h_actual * eta_mech)
            required_inlets[steam_id] = req_flow
            m_steam = req_flow

        power_generated_kw = (m_steam / 3600.0) * delta_h_actual * eta_mech

        # Exhaust steam stream
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
                "power_generated_kw": round(power_generated_kw, 2),
            },
            warnings=warnings,
            required_inlet_flows=required_inlets,
        )
