"""
solver/stations/process_units.py
Purity for Sugar — Reactor, Separator/Filter, and Dryer Station Models

Rules:
  - Reactor: stoichiometric conversion, ColorChange on NS#1 only (RULES_v5.md §A10), can explicitly set sol_coef_a,b,c (RULES_v5.md §A11)
  - Separator/Filter: splits insolubles into cake/mud and clarified liquid; color split (RULES_v5.md §A10)
  - Dryer: dries product to target dry matter %; evaporates water to vapor outlet
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream, mix_streams


class ReactorStation(BaseStation):
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
                warnings=["Reactor has no inlet flows."],
            )

        inlets = [inlet_streams[fid] for fid in inlet_flow_ids if fid in inlet_streams]
        in_stream = mix_streams(inlets)

        out_stream = in_stream.copy()

        # Solubility coefficient overrides (RULES_v5.md §A11: Reactor can explicitly set new coefficients)
        a_spec = self.get_float("sol_coef_a", -999.0)
        b_spec = self.get_float("sol_coef_b", -999.0)
        c_spec = self.get_float("sol_coef_c", -999.0)
        if a_spec > -200.0:
            out_stream.sol_coef_a = a_spec
        if b_spec > -200.0:
            out_stream.sol_coef_b = b_spec
        if c_spec > -200.0:
            out_stream.sol_coef_c = c_spec

        # Color change (RULES_v5.md §A10: applied to N.S. #1 only; if N.S. #1 = 0 -> no effect)
        color_change = self.get_float("color_change_cu", 0.0)
        if color_change != 0.0 and out_stream.non_sucrose_1 > 1e-6:
            out_stream.color_icu = max(0.0, out_stream.color_icu + color_change)

        # Reaction conversion (e.g. CaO slaking or Carbonatation: CaO + CO2 -> CaCO3)
        rxn_eff = self.get_float("reaction_eff_pct", 100.0) / 100.0
        delta_h_rxn = self.get_float("heat_reaction_kjkg", 0.0)

        if out_stream.cao > 1e-6 and rxn_eff > 0.0:
            # Conversion of CaO to CaCO3
            reacted_cao = out_stream.cao * rxn_eff
            out_stream.cao -= reacted_cao
            # 56 g CaO -> 100 g CaCO3
            out_stream.caco3 += reacted_cao * (100.0 / 56.0)
            out_stream.normalize()

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
                "out_flow_kgh": out_stream.mass_flow_kgh,
                "color_icu": out_stream.color_icu,
                "sol_coef_a": out_stream.sol_coef_a,
                "sol_coef_b": out_stream.sol_coef_b,
                "sol_coef_c": out_stream.sol_coef_c,
            },
            warnings=warnings,
        )


class SeparatorFilterStation(BaseStation):
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
                warnings=["Separator/Filter has no inlet flows."],
            )

        inlets = [inlet_streams[fid] for fid in inlet_flow_ids if fid in inlet_streams]
        in_stream = mix_streams(inlets)

        m_in = in_stream.mass_flow_kgh
        if m_in <= 1e-9:
            return StationResult(
                outlet_streams={ofid: Stream() for ofid in outlet_flow_ids},
                warnings=warnings,
            )

        # Split ratio: out_flow_1_pct is clarified juice/filtrate percentage
        split_pct = self.get_float("out_flow_1_pct", 85.0)
        frac_clarified = max(0.05, min(0.98, split_pct / 100.0))
        frac_mud = 1.0 - frac_clarified

        m_clarified = m_in * frac_clarified
        m_mud = m_in * frac_mud

        # Insoluble components (fiber, cao, caco3) concentrate heavily in mud (cake)
        # Typically 95% of insolubles go to mud
        insoluble_in_clarified = 0.05
        insoluble_in_mud = 0.95

        fiber_clarified = (in_stream.fiber_isns * m_in * insoluble_in_clarified) / m_clarified if m_clarified > 0 else 0.0
        fiber_mud = (in_stream.fiber_isns * m_in * insoluble_in_mud) / m_mud if m_mud > 0 else 0.0

        caco3_clarified = (in_stream.caco3 * m_in * insoluble_in_clarified) / m_clarified if m_clarified > 0 else 0.0
        caco3_mud = (in_stream.caco3 * m_in * insoluble_in_mud) / m_mud if m_mud > 0 else 0.0

        # Soluble sugars and water distribute with the liquid phase
        clarified_stream = in_stream.copy()
        clarified_stream.mass_flow_kgh = m_clarified
        clarified_stream.fiber_isns = fiber_clarified
        clarified_stream.caco3 = caco3_clarified
        clarified_stream.normalize()

        mud_stream = in_stream.copy()
        mud_stream.mass_flow_kgh = m_mud
        mud_stream.fiber_isns = fiber_mud
        mud_stream.caco3 = caco3_mud
        mud_stream.normalize()

        outlet_streams = {}
        if len(outlet_flow_ids) == 1:
            outlet_streams[outlet_flow_ids[0]] = clarified_stream
        elif len(outlet_flow_ids) >= 2:
            outlet_streams[outlet_flow_ids[0]] = clarified_stream
            outlet_streams[outlet_flow_ids[1]] = mud_stream
            for ofid in outlet_flow_ids[2:]:
                outlet_streams[ofid] = Stream()

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "clarified_flow_kgh": round(m_clarified, 2),
                "mud_flow_kgh": round(m_mud, 2),
                "insoluble_removal_pct": 95.0,
            },
            warnings=warnings,
        )


class DryerStation(BaseStation):
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
                warnings=["Dryer has no inlet flows."],
            )

        inlets = [inlet_streams[fid] for fid in inlet_flow_ids if fid in inlet_streams]
        in_stream = mix_streams(inlets)

        m_in = in_stream.mass_flow_kgh
        if m_in <= 1e-9:
            return StationResult(
                outlet_streams={ofid: Stream() for ofid in outlet_flow_ids},
                warnings=warnings,
            )

        target_dm_pct = self.get_float("dry_matter_out_pct", 99.8)
        target_dm = min(0.9995, max(in_stream.tdm_fraction, target_dm_pct / 100.0))
        t_out = self.get_float("temperature_out_c", 45.0)

        # Mass balance on dry solids
        solids_in = m_in * in_stream.tdm_fraction
        m_dried = solids_in / target_dm if target_dm > 0 else m_in
        m_evap = max(0.0, m_in - m_dried)

        # Dried product
        scale_dry = m_in / m_dried if m_dried > 0 else 1.0
        dried_stream = in_stream.copy()
        dried_stream.mass_flow_kgh = m_dried
        dried_stream.temperature_c = t_out
        dried_stream.water = max(0.0005, 1.0 - target_dm)
        dried_stream.dissolved_sucrose *= scale_dry
        dried_stream.sucrose_crystals *= scale_dry
        dried_stream.normalize()

        # Evaporated water vapor / exhaust air
        vapor_stream = Stream(
            mass_flow_kgh=m_evap,
            temperature_c=max(t_out, 60.0),
            pressure_kpa=atmospheric_p_kpa,
            water=0.0,
            water_vapor=1.0,
        ).normalize()

        outlet_streams = {}
        if len(outlet_flow_ids) == 1:
            outlet_streams[outlet_flow_ids[0]] = dried_stream
        elif len(outlet_flow_ids) >= 2:
            outlet_streams[outlet_flow_ids[0]] = dried_stream
            outlet_streams[outlet_flow_ids[1]] = vapor_stream
            for ofid in outlet_flow_ids[2:]:
                outlet_streams[ofid] = Stream()

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "dried_product_flow_kgh": round(m_dried, 2),
                "dried_matter_pct": round(dried_stream.tdm_pct, 2),
                "water_evaporated_kgh": round(m_evap, 2),
            },
            warnings=warnings,
        )
