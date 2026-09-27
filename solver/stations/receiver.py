"""
solver/stations/receiver.py
Purity for Sugar — Receiver Station Model

Rules:
  - Mixes all input streams (RULES_v5.md §A8, §A11)
  - Output pressure = MINIMUM of all input pressures (external flows with 0 flow ignored)
  - Weight-weighted solubility coefficients and color
  - Enthalpy and mass conservation
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream, mix_streams


class ReceiverStation(BaseStation):
    def calculate(
        self,
        inlet_streams: Dict[str, Stream],
        inlet_flow_ids: List[str],
        outlet_flow_ids: List[str],
        atmospheric_p_kpa: float = 101.325,
    ) -> StationResult:
        warnings = []
        if not inlet_flow_ids:
            warnings.append(f"Receiver {self.station_number} has no inlet flows.")
            out_stream = Stream(mass_flow_kgh=0.0, temperature_c=20.0, pressure_kpa=atmospheric_p_kpa)
        else:
            inlets = [inlet_streams[fid] for fid in inlet_flow_ids if fid in inlet_streams]
            # Receiver output pressure is MINIMUM of all active inputs (RULES_v5.md §A8)
            active_p = [s.pressure_kpa for s in inlets if s.mass_flow_kgh > 1e-6]
            if not active_p:
                active_p = [s.pressure_kpa for s in inlets] or [atmospheric_p_kpa]
            min_p = min(active_p)
            out_stream = mix_streams(inlets, pressure_mode="minimum")
            out_stream.pressure_kpa = min_p

        outlet_streams = {}
        if outlet_flow_ids:
            # If multiple outlets from a receiver, divide flow evenly or duplicate composition
            n_out = len(outlet_flow_ids)
            for ofid in outlet_flow_ids:
                s_copy = out_stream.copy()
                s_copy.mass_flow_kgh = out_stream.mass_flow_kgh / n_out
                outlet_streams[ofid] = s_copy

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "total_flow_kgh": out_stream.mass_flow_kgh,
                "ds_pct": out_stream.ds_pct,
                "purity_pct": out_stream.purity_pct,
                "temperature_c": out_stream.temperature_c,
                "pressure_kpa": out_stream.pressure_kpa,
            },
            warnings=warnings,
        )
