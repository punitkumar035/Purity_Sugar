"""
solver/stations/crystallizer.py
Purity for Sugar — Crystallizer Station Model

Rules:
  - Cooling massecuite drives crystal growth (RULES_v5.md §A9)
  - Crystals GROW as temperature drops, reducing mother liquor purity toward target supersaturation
  - Total mass and dry substance strictly conserved (closed cooling vessel)
  - Heat removal duty calculated: Q_cool = m * (h_in - h_out) + delta_crystals * 54.9 kJ/kg
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream, mix_streams
from engine.crystals import crystals_forward
from engine.enthalpy import heat_of_crystallization_kJkg


class CrystallizerStation(BaseStation):
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
                warnings=["Crystallizer has no inlet flows."],
            )

        inlets = [inlet_streams[fid] for fid in inlet_flow_ids if fid in inlet_streams]
        in_stream = mix_streams(inlets)

        m_in = in_stream.mass_flow_kgh
        if m_in <= 1e-9:
            return StationResult(
                outlet_streams={ofid: Stream() for ofid in outlet_flow_ids},
                warnings=warnings,
            )

        target_ss = self.get_float("supersaturation", 1.05)
        t_out_target = self.get_float("temperature_out_c", 45.0)
        color_rise = self.get_float("color_rise", 0.0)

        # Inherit or override solubility coefficients (RULES_v5.md §A11)
        a_coef = self.get_float("sol_coef_a", in_stream.sol_coef_a)
        b_coef = self.get_float("sol_coef_b", in_stream.sol_coef_b)
        c_coef = self.get_float("sol_coef_c", in_stream.sol_coef_c)

        # Crystal growth calculation at lower temperature
        ds_mc = in_stream.ds_fraction
        purity_mc = in_stream.purity_fraction
        t_cool = min(in_stream.temperature_c, t_out_target)

        cryst_result = crystals_forward(
            ds_mc=ds_mc,
            pu_mc=purity_mc,
            temp_c=t_cool,
            ss=target_ss,
            a=a_coef,
            b=b_coef,
            c=c_coef,
        )

        initial_cryst_frac = in_stream.crystal_fraction
        final_cryst_frac = max(initial_cryst_frac, cryst_result["crystal_frac"])
        delta_cryst_frac = final_cryst_frac - initial_cryst_frac
        delta_cryst_kgh = m_in * delta_cryst_frac

        ds_ml = cryst_result["ds_ml"]
        purity_ml = cryst_result["pu_ml"]

        # Formulate cooled massecuite stream
        out_stream = in_stream.copy()
        out_stream.temperature_c = t_cool
        out_stream.sucrose_crystals = final_cryst_frac
        out_stream.dissolved_sucrose = max(0.0, out_stream.dissolved_sucrose - delta_cryst_frac)
        out_stream.color_icu += color_rise
        out_stream.sol_coef_a = a_coef
        out_stream.sol_coef_b = b_coef
        out_stream.sol_coef_c = c_coef
        out_stream.normalize()

        # Heat balance: sensible cooling + latent heat of crystallization
        q_sensible = m_in * max(0.0, in_stream.enthalpy_kjkg - out_stream.enthalpy_kjkg)
        q_cryst = delta_cryst_kgh * heat_of_crystallization_kJkg()
        q_cool_total_kjh = q_sensible + q_cryst

        outlet_streams = {}
        if outlet_flow_ids:
            n_out = len(outlet_flow_ids)
            for ofid in outlet_flow_ids:
                s = out_stream.copy()
                s.mass_flow_kgh = m_in / n_out
                outlet_streams[ofid] = s

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "massecuite_flow_kgh": m_in,
                "inlet_temp_c": in_stream.temperature_c,
                "cooled_temp_c": t_cool,
                "initial_crystal_pct": round(initial_cryst_frac * 100.0, 2),
                "final_crystal_pct": round(final_cryst_frac * 100.0, 2),
                "additional_crystals_grown_kgh": round(delta_cryst_kgh, 2),
                "exhausted_mother_liquor_purity_pct": round(purity_ml * 100.0, 2),
                "cooling_heat_load_kw": round(q_cool_total_kjh / 3600.0, 2),
            },
            warnings=warnings,
        )
