"""
solver/stations/pressure_reducer.py
Purity for Sugar — Pressure Reducer / Expansion Valve Station Model

Rules:
  - Isenthalpic throttling: enthalpy is strictly conserved across the valve (h_in = h_out)
  - Drops pressure to pressure_out_kpa or by pressure_drop_kpa
  - For steam, slight superheating or moisture change occurs at constant enthalpy
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream, mix_streams


class PressureReducerStation(BaseStation):
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
                warnings=["Pressure reducer has no inlet flows."],
            )

        inlets = [inlet_streams[fid] for fid in inlet_flow_ids if fid in inlet_streams]
        in_stream = mix_streams(inlets)

        p_spec = self.get_float("pressure_out_kpa", -1.0)
        p_drop = self.get_float("pressure_drop_kpa", -1.0)

        p_out = in_stream.pressure_kpa
        if p_spec > 0.0:
            p_out = p_spec
        elif p_drop > 0.0:
            p_out = max(1.0, in_stream.pressure_kpa - p_drop)

        out_stream = in_stream.copy()
        out_stream.pressure_kpa = p_out

        # Isenthalpic throttling: for liquid, temperature change is negligible.
        # For steam, throttling causes Joule-Thomson temperature variation,
        # but at low pressure steam enthalpy h is mostly constant.
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
                "reduced_pressure_kpa": p_out,
                "pressure_drop_kpa": in_stream.pressure_kpa - p_out,
            },
            warnings=warnings,
        )
