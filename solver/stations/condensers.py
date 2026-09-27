"""
solver/stations/condensers.py
Purity for Sugar — Contact Condenser & Surface Condenser Models

Rules:
  - Contact condenser output is ALWAYS at atmospheric pressure (RULES_v5.md §A8)
  - Contact condenser cold water (port 1) is ALWAYS a required flow (RULES_v5.md §A7)
  - Heat balance determines minimum cooling water demand based on approach temperature
  - Surface condenser keeps condensate separate from warmed cooling water
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream, mix_streams
from engine.fluids import water_sat_temp_c, water_enthalpy_kJkg


class ContactCondenserStation(BaseStation):
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
                outlet_streams={ofid: Stream(pressure_kpa=atmospheric_p_kpa) for ofid in outlet_flow_ids},
                warnings=["Contact condenser has no inlet flows."],
            )

        # Port 0: Vapor inlet, Port 1: Cold water inlet (ALWAYS REQUIRED §A7)
        vap_id = inlet_flow_ids[0]
        vap_in = inlet_streams.get(vap_id, Stream()).copy()

        cw_id = inlet_flow_ids[1] if len(inlet_flow_ids) > 1 else None
        cw_in = inlet_streams.get(cw_id, Stream()).copy() if cw_id else None

        p_int = self.get_float("internal_pressure_kpa", 15.0)
        approach = self.get_float("approach_c", 5.0)
        t_sat = water_sat_temp_c(p_int)
        t_out_target = max(20.0, t_sat - approach)

        m_vap = vap_in.mass_flow_kgh
        h_vap = vap_in.enthalpy_kjkg if m_vap > 0 else water_enthalpy_kJkg(t_sat, p_int, quality=1.0)
        h_out = water_enthalpy_kJkg(t_out_target, p_int, quality=0.0)

        # Cooling water calculation
        t_cw_in = cw_in.temperature_c if cw_in else 28.0
        cp_w = 4.184
        delta_t_cw = max(2.0, t_out_target - t_cw_in)
        heat_to_absorb = m_vap * max(500.0, h_vap - h_out)
        req_cw = heat_to_absorb / (cp_w * delta_t_cw)

        if cw_id:
            required_inlets[cw_id] = req_cw

        m_cw_actual = req_cw
        total_out_flow = m_vap + m_cw_actual

        # Formulate tailpipe discharge stream (direct contact mixing at atmospheric pressure §A8)
        tailpipe_stream = Stream(
            mass_flow_kgh=total_out_flow,
            temperature_c=t_out_target,
            pressure_kpa=atmospheric_p_kpa,  # ALWAYS atmospheric §A8
            water=1.0,
            water_vapor=0.0,
        ).normalize()

        outlet_streams = {}
        if outlet_flow_ids:
            n_out = len(outlet_flow_ids)
            for ofid in outlet_flow_ids:
                s = tailpipe_stream.copy()
                s.mass_flow_kgh = total_out_flow / n_out
                outlet_streams[ofid] = s

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "internal_pressure_kpa": p_int,
                "saturation_temp_c": round(t_sat, 2),
                "tailpipe_temp_c": round(t_out_target, 2),
                "vapor_condensed_kgh": round(m_vap, 2),
                "cooling_water_kgh": round(m_cw_actual, 2),
                "water_to_vapor_ratio": round(m_cw_actual / m_vap, 1) if m_vap > 0 else 0.0,
            },
            warnings=warnings,
            required_inlet_flows=required_inlets,
        )


class SurfaceCondenserStation(BaseStation):
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
                warnings=["Surface condenser has no inlet flows."],
            )

        vap_id = inlet_flow_ids[0]
        vap_in = inlet_streams.get(vap_id, Stream()).copy()

        cw_id = inlet_flow_ids[1] if len(inlet_flow_ids) > 1 else None
        cw_in = inlet_streams.get(cw_id, Stream()).copy() if cw_id else None

        p_int = self.get_float("internal_pressure_kpa", 15.0)
        t_drop = self.get_float("temperature_drop_c", 2.0)
        t_sat = water_sat_temp_c(p_int)
        t_cond = max(20.0, t_sat - t_drop)

        m_vap = vap_in.mass_flow_kgh
        h_vap = vap_in.enthalpy_kjkg if m_vap > 0 else water_enthalpy_kJkg(t_sat, p_int, quality=1.0)
        h_cond = water_enthalpy_kJkg(t_cond, p_int, quality=0.0)

        # Duty: Q = m_vap * (h_vap - h_cond)
        q_duty_kjh = m_vap * max(500.0, h_vap - h_cond)

        t_cw_in = cw_in.temperature_c if cw_in else 28.0
        delta_t_cw = 8.0
        t_cw_out = t_cw_in + delta_t_cw
        cp_w = 4.184
        req_cw = q_duty_kjh / (cp_w * delta_t_cw)

        if cw_id:
            required_inlets[cw_id] = req_cw

        # Outlet 0: Condensate; Outlet 1: Warmed Cooling Water
        cond_stream = Stream(
            mass_flow_kgh=m_vap,
            temperature_c=t_cond,
            pressure_kpa=p_int,
            water=1.0,
            water_vapor=0.0,
        ).normalize()

        cw_out_stream = Stream(
            mass_flow_kgh=req_cw,
            temperature_c=t_cw_out,
            pressure_kpa=cw_in.pressure_kpa if cw_in else atmospheric_p_kpa,
            water=1.0,
            water_vapor=0.0,
        ).normalize()

        outlet_streams = {}
        if len(outlet_flow_ids) == 1:
            outlet_streams[outlet_flow_ids[0]] = cond_stream
        elif len(outlet_flow_ids) >= 2:
            outlet_streams[outlet_flow_ids[0]] = cond_stream
            outlet_streams[outlet_flow_ids[1]] = cw_out_stream
            for ofid in outlet_flow_ids[2:]:
                outlet_streams[ofid] = Stream()

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "internal_pressure_kpa": p_int,
                "condensate_flow_kgh": round(m_vap, 2),
                "condensate_temp_c": round(t_cond, 2),
                "cooling_water_flow_kgh": round(req_cw, 2),
                "cooling_water_out_temp_c": round(t_cw_out, 2),
                "duty_kw": round(q_duty_kjh / 3600.0, 2),
            },
            warnings=warnings,
            required_inlet_flows=required_inlets,
        )
