"""
solver/stations/cooler.py
Purity for Sugar — Fluid Cooler Station Model

Rules:
  - Sensible cooling by temperature_drop_k or target temperature_out_c
  - Heat removal duty: Q_removed = m * (h_in - h_out)
  - NO crystal growth: liquid may become supersaturated (RULES_v5.md §A9)
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream, mix_streams


class CoolerStation(BaseStation):
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
                warnings=["Cooler has no inlet flows."],
            )

        inlets = [inlet_streams[fid] for fid in inlet_flow_ids if fid in inlet_streams]
        in_stream = mix_streams(inlets)

        t_drop = self.get_float("temperature_drop_k", -1.0)
        t_out_spec = self.get_float("temperature_out_c", -999.0)

        t_out = in_stream.temperature_c
        if t_out_spec > -200.0:
            t_out = t_out_spec
        elif t_drop > 0.0:
            t_out = max(0.0, in_stream.temperature_c - t_drop)

        out_stream = in_stream.copy()
        out_stream.temperature_c = t_out

        q_duty_kjh = in_stream.mass_flow_kgh * max(0.0, in_stream.enthalpy_kjkg - out_stream.enthalpy_kjkg)

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
                "cooling_duty_kw": round(q_duty_kjh / 3600.0, 2),
                "temp_in_c": in_stream.temperature_c,
                "temp_out_c": t_out,
                "supersaturation_out": out_stream.supersaturation,
            },
            warnings=warnings,
        )
