"""
solver/stations/centrifugal.py
Purity for Sugar — Centrifugal Station Model

Rules:
  - ALL outputs are ALWAYS at atmospheric pressure (RULES_v5.md §A8)
  - 2-output configuration: Sugar (Port 0) + Combined Molasses (Port 1)
  - 3-output configuration: Sugar (Port 0) + Green Syrup (Port 1) + Wash Syrup (Port 2)
  - Wash water dissolves a small fraction of crystals (typically 2-8%)
  - Color and solubility coefficients calculated per RULES_v5.md §A10, §A11
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream


class CentrifugalStation(BaseStation):
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
                outlet_streams={ofid: Stream(pressure_kpa=atmospheric_p_kpa) for ofid in outlet_flow_ids},
                warnings=["Centrifugal has no inlet flows."],
            )

        # Port 0: Massecuite feed
        mc_id = inlet_flow_ids[0]
        mc_in = inlet_streams.get(mc_id, Stream()).copy()

        # Port 1: Wash water / steam feed
        wash_id = inlet_flow_ids[1] if len(inlet_flow_ids) > 1 else None
        wash_in = inlet_streams.get(wash_id, Stream()).copy() if wash_id else None

        m_mc = mc_in.mass_flow_kgh
        if m_mc <= 1e-9:
            return StationResult(
                outlet_streams={ofid: Stream(pressure_kpa=atmospheric_p_kpa) for ofid in outlet_flow_ids},
                warnings=warnings,
            )

        m_wash = wash_in.mass_flow_kgh if wash_in else 0.0
        t_wash = wash_in.temperature_c if wash_in else 80.0

        # Massecuite properties
        cryst_frac_in = mc_in.crystal_fraction
        m_cryst_in = m_mc * cryst_frac_in
        m_ml_in = max(0.0, m_mc - m_cryst_in)

        # Mother liquor composition
        scale_ml = 1.0 / (1.0 - cryst_frac_in) if (1.0 - cryst_frac_in) > 1e-6 else 1.0
        ml_ds_frac = mc_in.ml_ds_fraction
        ml_purity_frac = mc_in.ml_purity_fraction

        # Target sugar product specifications
        sugar_ds_pct = self.get_float("sugar_ds_pct", 99.2)
        sugar_purity_pct = self.get_float("sugar_purity_pct", 99.5)
        sugar_temp_c = self.get_float("sugar_temp_c", mc_in.temperature_c)

        # Wash parameters
        wash_quality_pct = self.get_float("wash_quality_pct", 95.0)  # displacement efficiency
        # Crystal dissolution by wash water: typically 0.25 to 0.4 kg sucrose dissolved per kg wash water
        cryst_dissolved = min(m_cryst_in * 0.15, m_wash * 0.35)
        m_cryst_retained = max(0.0, m_cryst_in - cryst_dissolved)

        # Sugar product stream: contains retained crystals + thin film of moisture
        sugar_ds = sugar_ds_pct / 100.0
        m_sugar_product = m_cryst_retained / sugar_ds if sugar_ds > 0 else m_cryst_retained
        water_in_sugar = max(0.0, m_sugar_product - m_cryst_retained)

        sugar_stream = Stream(
            mass_flow_kgh=m_sugar_product,
            temperature_c=sugar_temp_c,
            pressure_kpa=atmospheric_p_kpa,
            water=water_in_sugar / m_sugar_product if m_sugar_product > 0 else 0.008,
            dissolved_sucrose=0.002,
            sucrose_crystals=m_cryst_retained / m_sugar_product if m_sugar_product > 0 else 0.99,
            non_sucrose_1=0.0005,
            non_sucrose_2=0.0005,
            color_icu=max(10.0, mc_in.color_icu * 0.05),
        ).normalize()

        # Run-off streams (Green syrup and Wash syrup)
        total_liquor_mass = (m_mc + m_wash) - m_sugar_product
        n_outlets = len(outlet_flow_ids)

        if n_outlets <= 2:
            # Combined Molasses / Run-off
            # All non-sugar components go into molasses
            m_molasses = max(0.0, total_liquor_mass)
            # Solute mass balances
            w_water_mol = max(0.0, (mc_in.water * m_mc + (wash_in.water * m_wash if wash_in else 0.0)) - water_in_sugar)
            w_ds_mol = max(0.0, (mc_in.ds_fraction * m_mc) - (sugar_stream.ds_fraction * m_sugar_product))

            molasses_stream = Stream(
                mass_flow_kgh=m_molasses,
                temperature_c=mc_in.temperature_c,
                pressure_kpa=atmospheric_p_kpa,
                water=w_water_mol / m_molasses if m_molasses > 0 else 0.20,
                dissolved_sucrose=max(0.0, (mc_in.dissolved_sucrose * m_mc + cryst_dissolved) / m_molasses) if m_molasses > 0 else 0.45,
                non_sucrose_1=(mc_in.non_sucrose_1 * m_mc) / m_molasses if m_molasses > 0 else 0.25,
                non_sucrose_2=(mc_in.non_sucrose_2 * m_mc) / m_molasses if m_molasses > 0 else 0.10,
                sucrose_crystals=0.0,  # crystals purged
                color_icu=(mc_in.color_icu * m_mc) / m_molasses if m_molasses > 0 else mc_in.color_icu * 1.5,
                sol_coef_a=mc_in.sol_coef_a,
                sol_coef_b=mc_in.sol_coef_b,
                sol_coef_c=mc_in.sol_coef_c,
            ).normalize()

            outlet_streams = {}
            if n_outlets == 1:
                outlet_streams[outlet_flow_ids[0]] = sugar_stream
            else:
                outlet_streams[outlet_flow_ids[0]] = sugar_stream
                outlet_streams[outlet_flow_ids[1]] = molasses_stream

        else:
            # 3-output separation: Sugar (0), Green Syrup (1), Wash Syrup (2)
            # Green syrup receives the pure mother liquor purged before washing (typically 80% of mother liquor)
            m_green = m_ml_in * 0.85
            m_wash_syrup = max(0.0, total_liquor_mass - m_green)

            green_stream = Stream(
                mass_flow_kgh=m_green,
                temperature_c=mc_in.temperature_c,
                pressure_kpa=atmospheric_p_kpa,
                water=mc_in.water * scale_ml,
                dissolved_sucrose=mc_in.dissolved_sucrose * scale_ml,
                non_sucrose_1=mc_in.non_sucrose_1 * scale_ml,
                non_sucrose_2=mc_in.non_sucrose_2 * scale_ml,
                sucrose_crystals=0.0,
                color_icu=mc_in.color_icu * 1.6,
                sol_coef_a=mc_in.sol_coef_a,
                sol_coef_b=mc_in.sol_coef_b,
                sol_coef_c=mc_in.sol_coef_c,
            ).normalize()

            # Wash syrup receives remaining mother liquor + dissolved crystal sugar + wash water
            wash_syrup_stream = Stream(
                mass_flow_kgh=m_wash_syrup,
                temperature_c=max(mc_in.temperature_c, t_wash),
                pressure_kpa=atmospheric_p_kpa,
                water=0.25,
                dissolved_sucrose=0.60,
                non_sucrose_1=0.12,
                non_sucrose_2=0.03,
                sucrose_crystals=0.0,
                color_icu=mc_in.color_icu * 0.6,
                sol_coef_a=mc_in.sol_coef_a,
                sol_coef_b=mc_in.sol_coef_b,
                sol_coef_c=mc_in.sol_coef_c,
            ).normalize()

            outlet_streams = {
                outlet_flow_ids[0]: sugar_stream,
                outlet_flow_ids[1]: green_stream,
                outlet_flow_ids[2]: wash_syrup_stream,
            }
            for ofid in outlet_flow_ids[3:]:
                outlet_streams[ofid] = Stream(pressure_kpa=atmospheric_p_kpa)

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "sugar_flow_kgh": round(sugar_stream.mass_flow_kgh, 2),
                "sugar_purity_pct": round(sugar_stream.purity_pct, 2),
                "crystals_recovered_kgh": round(m_cryst_retained, 2),
                "crystals_dissolved_by_wash_kgh": round(cryst_dissolved, 2),
                "total_molasses_flow_kgh": round(total_liquor_mass, 2),
            },
            warnings=warnings,
        )
