"""
solver/stations/blender.py
Purity for Sugar — Blender / Mingler Station Model

Rules:
  - 2 or more inlet flows mixed according to specified ratio or target outlet condition
  - May dissolve crystals if undersaturated (RULES_v5.md §A9)
  - Weight-weighted average solubility coefficients (RULES_v5.md §A11)
  - Blender blend input (port 1) is required flow if target ratio or target DS is specified (RULES_v5.md §A7)
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream, mix_streams
from engine.crystals import crystals_forward


class BlenderStation(BaseStation):
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
                warnings=["Blender has no inlet flows."],
            )

        # Primary flow is first inlet, secondary blend flow is second inlet
        primary_id = inlet_flow_ids[0]
        primary_stream = inlet_streams.get(primary_id, Stream())

        blend_id = inlet_flow_ids[1] if len(inlet_flow_ids) > 1 else None
        blend_stream = inlet_streams.get(blend_id, Stream()) if blend_id else None

        ratio = self.get_float("ratio", -1.0)
        target_ds_pct = self.get_float("ds_out_pct", -1.0)
        target_qty = self.get_float("quantity_out_kgh", -1.0)
        spec_blend_qty = self.get_float("blend_quantity_kgh", -1.0)

        # 1. Check if blend flow needs to be calculated (required flow)
        if blend_id is not None:
            if spec_blend_qty > 0.0:
                required_inlets[blend_id] = spec_blend_qty
            elif ratio > 0.0 and primary_stream.mass_flow_kgh > 0.0:
                # ratio = blend_flow / primary_flow
                req_blend = primary_stream.mass_flow_kgh * ratio
                required_inlets[blend_id] = req_blend
            elif target_ds_pct > 0.0 and primary_stream.mass_flow_kgh > 0.0:
                target_ds = target_ds_pct / 100.0
                ds_p = primary_stream.ds_fraction
                ds_b = blend_stream.ds_fraction if blend_stream else 0.0
                # ds_out = (m_p * ds_p + m_b * ds_b) / (m_p + m_b) = target_ds
                # m_b * (target_ds - ds_b) = m_p * (ds_p - target_ds)
                denom = target_ds - ds_b
                if abs(denom) > 1e-4:
                    req_blend = max(0.0, primary_stream.mass_flow_kgh * (ds_p - target_ds) / denom)
                    required_inlets[blend_id] = req_blend
            elif target_qty > 0.0:
                req_blend = max(0.0, target_qty - primary_stream.mass_flow_kgh)
                required_inlets[blend_id] = req_blend

        # Active inlet streams
        active_inlets = []
        for fid in inlet_flow_ids:
            if fid in inlet_streams:
                st = inlet_streams[fid].copy()
                if fid in required_inlets:
                    st.mass_flow_kgh = required_inlets[fid]
                active_inlets.append(st)

        # Mix streams
        mixed = mix_streams(active_inlets, pressure_mode="minimum")

        # 2. Check crystal dissolution (RULES_v5.md §A9)
        # In blender, if mixture is undersaturated (Ss < 1.0) and crystals are present, crystals dissolve
        if mixed.crystal_fraction > 1e-5:
            # Check solubility at mixture temp
            ss = mixed.supersaturation
            if ss < 0.9999 and mixed.water > 1e-5:
                # Dissolve crystals until Ss=1.0 or crystals exhausted
                # Mother liquor can hold more sucrose:
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
                    new_cryst_frac = max(0.0, res["crystal_frac"])
                    dissolved_cryst = max(0.0, mixed.crystal_fraction - new_cryst_frac)
                    mixed.sucrose_crystals = new_cryst_frac
                    mixed.dissolved_sucrose += dissolved_cryst
                    mixed.normalize()
                except Exception:
                    pass

        # Optional forced temperature out
        target_temp = self.get_float("temperature_out_c", -999.0)
        if target_temp > -200.0:
            mixed.temperature_c = target_temp

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
                "mixed_flow_kgh": mixed.mass_flow_kgh,
                "mixed_ds_pct": mixed.ds_pct,
                "mixed_purity_pct": mixed.purity_pct,
                "mixed_temp_c": mixed.temperature_c,
                "mixed_crystal_pct": mixed.crystal_pct,
            },
            warnings=warnings,
            required_inlet_flows=required_inlets,
        )
