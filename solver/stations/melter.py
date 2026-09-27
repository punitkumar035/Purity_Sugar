"""
solver/stations/melter.py
Purity for Sugar — Sugar Melter Station Model

Rules:
  - Completely dissolves sucrose crystals into solution: crystals -> 0.0 (RULES_v5.md §A9)
  - Output pressure is ALWAYS atmospheric (RULES_v5.md §A8)
  - Melter dilution (port 9) is required flow when hold_tdm_pct is specified (RULES_v5.md §A7)
  - Melter heating medium (port 10) is required flow when connected and temp specified (RULES_v5.md §A7)
  - Endothermic heat of dissolution (-54.9 kJ/kg) included in energy balance
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream, mix_streams
from engine.fluids import water_sat_temp_c, water_enthalpy_kJkg
from engine.enthalpy import heat_of_dissolution_kJkg


class MelterStation(BaseStation):
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
                warnings=["Melter has no inlet flows."],
            )

        # Port 0: Sugar feed (crystals)
        sugar_in_id = inlet_flow_ids[0]
        sugar_in = inlet_streams.get(sugar_in_id, Stream()).copy()

        # Port 9: Dilution sweetwater/water
        dilution_in_id = inlet_flow_ids[1] if len(inlet_flow_ids) > 1 else None
        dilution_in = inlet_streams.get(dilution_in_id, Stream()).copy() if dilution_in_id else None

        # Port 10: Heating medium (steam)
        steam_in_id = inlet_flow_ids[2] if len(inlet_flow_ids) > 2 else None
        steam_in = inlet_streams.get(steam_in_id, Stream()).copy() if steam_in_id else None

        hold_tdm_pct = self.get_float("hold_tdm_pct", 65.0)
        t_out_target = self.get_float("temperature_out_c", 75.0)
        color_rise = self.get_float("color_rise", 0.0)
        heat_loss_pct = self.get_float("heat_loss_pct", 2.0)
        heat_eff = max(0.01, 1.0 - heat_loss_pct / 100.0)

        # 1. Dilution calculation to reach hold_tdm_pct (RULES_v5.md §A7)
        target_tdm = hold_tdm_pct / 100.0
        m_sugar = sugar_in.mass_flow_kgh
        s_tdm = sugar_in.tdm_fraction

        m_dilution = dilution_in.mass_flow_kgh if dilution_in else 0.0
        d_tdm = dilution_in.tdm_fraction if dilution_in else 0.0

        if dilution_in_id and m_sugar > 0:
            if target_tdm < s_tdm and abs(target_tdm - d_tdm) > 1e-4:
                req_dilution = max(0.0, m_sugar * (s_tdm - target_tdm) / (target_tdm - d_tdm))
                required_inlets[dilution_in_id] = req_dilution
                m_dilution = req_dilution
                if dilution_in:
                    dilution_in.mass_flow_kgh = req_dilution

        # Mix sugar feed and dilution water
        process_inlets = [sugar_in]
        if dilution_in and m_dilution > 0:
            d_st = dilution_in.copy()
            d_st.mass_flow_kgh = m_dilution
            process_inlets.append(d_st)

        melt_stream = mix_streams(process_inlets, pressure_mode="minimum")

        # 2. Complete Crystal Dissolution (RULES_v5.md §A9)
        # All crystals converted to dissolved sucrose
        cryst_fraction = melt_stream.crystal_fraction
        cryst_kgh = melt_stream.mass_flow_kgh * cryst_fraction
        melt_stream.dissolved_sucrose += melt_stream.sucrose_crystals
        melt_stream.sucrose_crystals = 0.0
        melt_stream.normalize()

        # Atmospheric pressure out (RULES_v5.md §A8)
        melt_stream.pressure_kpa = atmospheric_p_kpa
        melt_stream.temperature_c = t_out_target
        if color_rise > 0:
            melt_stream.color_icu += color_rise

        # 3. Heating Duty & Steam Consumption (RULES_v5.md §A7)
        # Heat required = Sensible heating of liquid + Endothermic heat of dissolution
        # Q_diss = m_cryst * |delta_h_diss| = cryst_kgh * 54.9 kJ/kg
        cp_melt = 3.3  # approx 65-70 Brix liquor Cp
        t_feed = sugar_in.temperature_c
        q_sensible = melt_stream.mass_flow_kgh * cp_melt * max(0.0, t_out_target - t_feed)
        q_diss = cryst_kgh * abs(heat_of_dissolution_kJkg())
        q_total_kjh = (q_sensible + q_diss) / heat_eff

        m_steam = 0.0
        t_cond = 95.0
        if steam_in_id:
            p_steam = steam_in.pressure_kpa if steam_in else 150.0
            t_sat = water_sat_temp_c(p_steam)
            h_steam = steam_in.enthalpy_kjkg if steam_in else water_enthalpy_kJkg(t_sat, p_steam, quality=1.0)
            t_cond = max(40.0, t_sat - 2.0)
            h_cond = water_enthalpy_kJkg(t_cond, p_steam, quality=0.0)
            latent = max(500.0, h_steam - h_cond)
            req_steam = q_total_kjh / latent
            required_inlets[steam_in_id] = req_steam
            m_steam = req_steam

        # Outlets: Port 0 = Melted liquor, Port 1 = Heating condensate (if present)
        outlet_streams = {}
        if len(outlet_flow_ids) == 1:
            outlet_streams[outlet_flow_ids[0]] = melt_stream
        elif len(outlet_flow_ids) >= 2:
            outlet_streams[outlet_flow_ids[0]] = melt_stream
            # Condensate outlet
            cond_stream = Stream(
                mass_flow_kgh=m_steam,
                temperature_c=t_cond,
                pressure_kpa=atmospheric_p_kpa,
                water=1.0,
                water_vapor=0.0,
            ).normalize()
            outlet_streams[outlet_flow_ids[1]] = cond_stream
            for ofid in outlet_flow_ids[2:]:
                outlet_streams[ofid] = Stream(pressure_kpa=atmospheric_p_kpa)

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "melt_flow_kgh": melt_stream.mass_flow_kgh,
                "melt_brix_pct": melt_stream.ds_pct,
                "melt_temp_c": melt_stream.temperature_c,
                "crystals_melted_kgh": cryst_kgh,
                "heat_duty_kw": round(q_total_kjh / 3600.0, 2),
                "steam_consumed_kgh": round(m_steam, 2),
            },
            warnings=warnings,
            required_inlet_flows=required_inlets,
        )
