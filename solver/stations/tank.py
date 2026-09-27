"""
solver/stations/tank.py
Purity for Sugar — Tank Station Model

Rules:
  - Output pressure is ALWAYS atmospheric (RULES_v5.md §A8)
  - Dilution to hold TDM: if hold_tdm_pct specified, dilution stream flow is required flow (RULES_v5.md §A7)
  - Dissolves crystals to Ss=1.0 if undersaturated, never grows (RULES_v5.md §A9)
  - Optional heating and color rise
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream, mix_streams
from engine.crystals import crystals_forward


class TankStation(BaseStation):
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
                warnings=["Tank has no inlet flows."],
            )

        # Primary process feed is first inlet
        primary_id = inlet_flow_ids[0]
        primary_stream = inlet_streams.get(primary_id, Stream()).copy()

        # Dilution feed if present (port 9 in Visio)
        dilution_id = inlet_flow_ids[1] if len(inlet_flow_ids) > 1 else None
        dilution_stream = inlet_streams.get(dilution_id, Stream()).copy() if dilution_id else None

        hold_tdm_pct = self.get_float("hold_tdm_pct", -1.0)
        target_t = self.get_float("temperature_out_c", -999.0)
        color_rise = self.get_float("color_rise", 0.0)

        # 1. Hold TDM dilution calculation
        if hold_tdm_pct > 0.0 and dilution_id and primary_stream.mass_flow_kgh > 0:
            target_tdm = hold_tdm_pct / 100.0
            p_tdm = primary_stream.tdm_fraction
            d_tdm = dilution_stream.tdm_fraction if dilution_stream else 0.0
            # Target TDM = (m_p * p_tdm + m_d * d_tdm) / (m_p + m_d)
            if target_tdm < p_tdm and abs(target_tdm - d_tdm) > 1e-4:
                req_dilution = max(0.0, primary_stream.mass_flow_kgh * (p_tdm - target_tdm) / (target_tdm - d_tdm))
                required_inlets[dilution_id] = req_dilution
                if dilution_stream:
                    dilution_stream.mass_flow_kgh = req_dilution

        active_inlets = []
        for fid in inlet_flow_ids:
            if fid in inlet_streams:
                st = inlet_streams[fid].copy()
                if fid in required_inlets:
                    st.mass_flow_kgh = required_inlets[fid]
                active_inlets.append(st)

        mixed = mix_streams(active_inlets, pressure_mode="minimum")

        # Atmospheric pressure out (RULES_v5.md §A8)
        mixed.pressure_kpa = atmospheric_p_kpa

        # Temperature override if tank is heated
        if target_t > -200.0:
            mixed.temperature_c = target_t

        # Color rise
        if color_rise > 0.0:
            mixed.color_icu += color_rise

        # Dissolve crystals if undersaturated (RULES_v5.md §A9)
        if mixed.crystal_fraction > 1e-5:
            ss = mixed.supersaturation
            if ss < 0.9999 and mixed.water > 1e-5:
                try:
                    res = crystals_forward(
                        ds_mc=mixed.ds_fraction,
                        pu_mc=mixed.purity_fraction,
                        temp_c=mixed.temperature_c,
                        ss=1.0,
                        a=mixed.sol_coef_a,
                        b=mixed.sol_coef_b,
                        c=mixed.sol_coef_c,
                    )
                    new_cryst = max(0.0, res["crystal_frac"])
                    diss = max(0.0, mixed.crystal_fraction - new_cryst)
                    mixed.sucrose_crystals = new_cryst
                    mixed.dissolved_sucrose += diss
                    mixed.normalize()
                except Exception:
                    pass

        outlet_streams = {}
        if outlet_flow_ids:
            n_out = len(outlet_flow_ids)
            for ofid in outlet_flow_ids:
                s = mixed.copy()
                s.mass_flow_kgh = mixed.mass_flow_kgh / n_out
                outlet_streams[ofid] = s

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "tank_flow_kgh": mixed.mass_flow_kgh,
                "ds_pct": mixed.ds_pct,
                "tdm_pct": mixed.tdm_pct,
                "temperature_c": mixed.temperature_c,
            },
            warnings=warnings,
            required_inlet_flows=required_inlets,
        )
