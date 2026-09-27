"""
solver/stations/pump.py
Purity for Sugar — Fluid Pump Station Model

Rules:
  - Raises fluid pressure to discharge_pressure_kpa or by pressure_rise_kpa
  - Fluid flow and composition preserved identically
  - Hydraulic power: P_hyd = m_dot * delta_P / (rho * eta)
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream, mix_streams


class PumpStation(BaseStation):
    def calculate(
        self,
        inlet_streams: Dict[str, Stream],
        inlet_flow_ids: List[str],
        outlet_flow_ids: List[str],
        atmospheric_p_kpa: float = 101.325,
    ) -> StationResult:
        warnings = []
        if not inlet_flow_ids:
            return StationResult(
                outlet_streams={ofid: Stream() for ofid in outlet_flow_ids},
                warnings=["Pump has no inlet flows."],
            )

        inlets = [inlet_streams[fid] for fid in inlet_flow_ids if fid in inlet_streams]
        in_stream = mix_streams(inlets)

        p_disch = self.get_float("discharge_pressure_kpa", -1.0)
        p_rise = self.get_float("pressure_rise_kpa", -1.0)

        p_out = in_stream.pressure_kpa
        if p_disch > 0.0:
            p_out = p_disch
        elif p_rise > 0.0:
            p_out = in_stream.pressure_kpa + p_rise

        out_stream = in_stream.copy()
        out_stream.pressure_kpa = max(1.0, p_out)

        # Hydraulic power calculation
        delta_p_kpa = max(0.0, p_out - in_stream.pressure_kpa)
        rho = max(500.0, in_stream.density_kgm3)
        # Volumetric flow m3/s = (kg/h / 3600) / rho
        v_flow_m3s = (in_stream.mass_flow_kgh / 3600.0) / rho
        # Power kW = V (m3/s) * delta_p (kPa)
        power_hyd_kw = v_flow_m3s * delta_p_kpa

        outlet_streams = {}
        if outlet_flow_ids:
            n_out = len(outlet_flow_ids)
            for ofid in outlet_flow_ids:
                s = out_stream.copy()
                s.mass_flow_kgh = out_stream.mass_flow_kgh / n_out
                outlet_streams[ofid] = s

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "inlet_pressure_kpa": in_stream.pressure_kpa,
                "discharge_pressure_kpa": p_out,
                "pressure_rise_kpa": delta_p_kpa,
                "hydraulic_power_kw": round(power_hyd_kw, 3),
            },
            warnings=warnings,
        )
