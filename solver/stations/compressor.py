"""
solver/stations/compressor.py
Purity for Sugar — Vapor / Gas Compressor (MVR) Station Model

Rules:
  - Compresses vapor/gas to higher discharge pressure (MVR)
  - Work input: W_comp = m_dot * (h_out - h_in)
  - Outflow carries compressed superheated vapor
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream, mix_streams
from engine.fluids import water_sat_temp_c


class CompressorStation(BaseStation):
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
                warnings=["Compressor has no inlet flows."],
            )

        inlets = [inlet_streams[fid] for fid in inlet_flow_ids if fid in inlet_streams]
        in_stream = mix_streams(inlets)

        p_disch = self.get_float("discharge_pressure_kpa", 150.0)
        t_disch_spec = self.get_float("discharge_temp_c", -999.0)

        t_sat_disch = water_sat_temp_c(p_disch)
        t_out = max(t_sat_disch, in_stream.temperature_c + 15.0)
        if t_disch_spec > -200.0:
            t_out = t_disch_spec

        out_stream = in_stream.copy()
        out_stream.pressure_kpa = p_disch
        out_stream.temperature_c = t_out

        # Compression power estimate
        delta_h = max(20.0, 2.0 * (t_out - in_stream.temperature_c))
        power_kw = (in_stream.mass_flow_kgh / 3600.0) * delta_h

        outlet_streams = {}
        if outlet_flow_ids:
            n_out = len(outlet_flow_ids)
            for ofid in outlet_flow_ids:
                s = out_stream.copy()
                s.mass_flow_kgh = in_stream.mass_flow_kgh / n_out
                outlet_streams[ofid] = s

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "inlet_pressure_kpa": in_stream.pressure_kpa,
                "discharge_pressure_kpa": p_disch,
                "compression_power_kw": round(power_kw, 2),
                "discharge_temp_c": round(t_out, 2),
            },
            warnings=warnings,
        )
