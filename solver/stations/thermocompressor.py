"""
solver/stations/thermocompressor.py
Purity for Sugar — Steam Jet Thermocompressor Station Model

Rules:
  - High pressure motive steam entrains low pressure suction vapor to produce intermediate pressure vapor
  - Entrainment ratio: R = m_suction / m_motive
  - Total discharge flow: m_discharge = m_motive + m_suction
  - Enthalpy conservation: m_disch * h_disch = m_mot * h_mot + m_suc * h_suc
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream, mix_streams


class ThermocompressorStation(BaseStation):
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
                warnings=["Thermocompressor has no inlet flows."],
            )

        # Port 0: Motive steam, Port 1: Suction vapor
        motive_id = inlet_flow_ids[0]
        motive_in = inlet_streams.get(motive_id, Stream()).copy()

        suction_id = inlet_flow_ids[1] if len(inlet_flow_ids) > 1 else None
        suction_in = inlet_streams.get(suction_id, Stream()).copy() if suction_id else None

        p_disch = self.get_float("pressure_out_kpa", 130.0)
        entrain_ratio = self.get_float("entrainment_ratio", -1.0)

        inlets = [motive_in]
        if suction_in:
            inlets.append(suction_in)

        disch_stream = mix_streams(inlets, pressure_mode="average")
        disch_stream.pressure_kpa = p_disch

        outlet_streams = {}
        if outlet_flow_ids:
            n_out = len(outlet_flow_ids)
            for ofid in outlet_flow_ids:
                s = disch_stream.copy()
                s.mass_flow_kgh = disch_stream.mass_flow_kgh / n_out
                outlet_streams[ofid] = s

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "motive_pressure_kpa": motive_in.pressure_kpa,
                "discharge_pressure_kpa": p_disch,
                "discharge_flow_kgh": disch_stream.mass_flow_kgh,
                "entrainment_ratio": round(suction_in.mass_flow_kgh / motive_in.mass_flow_kgh, 2) if (suction_in and motive_in.mass_flow_kgh > 0) else 0.0,
            },
            warnings=warnings,
        )
