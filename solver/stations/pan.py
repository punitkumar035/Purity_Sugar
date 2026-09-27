"""
solver/stations/pan.py
Purity for Sugar — Vacuum Pan Station Model

Rules:
  - Pan steam input (port 1) is ALWAYS a required flow (RULES_v5.md §A7)
  - Pan vapor out and condensate out CANNOT be required (RULES_v5.md §A7)
  - Sucrose crystals GROW from supersaturation (RULES_v5.md §A9)
  - Exothermic heat of crystallization (+54.9 kJ/kg) included in energy balance (RULES_v5.md §B7)
  - Crystal yield and mother liquor equilibrium computed via authentic Vavrinecz solubility (RULES_v5.md §B4)
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream
from engine.fluids import water_sat_temp_c, water_sat_pressure_kpa, water_enthalpy_kJkg
from engine.bpe import bpe_celsius
from engine.crystals import crystals_forward
from engine.enthalpy import heat_of_crystallization_kJkg


class PanStation(BaseStation):
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
                warnings=["Pan has no inlet flows."],
            )

        # Port 0: Feed syrup/molasses
        feed_id = inlet_flow_ids[0]
        feed_in = inlet_streams.get(feed_id, Stream()).copy()

        # Port 1: Calandria heating steam (ALWAYS required flow §A7)
        steam_id = inlet_flow_ids[1] if len(inlet_flow_ids) > 1 else None
        steam_in = inlet_streams.get(steam_id, Stream()).copy() if steam_id else None

        # Configuration properties
        p_vap = self.get_float("vapor_pressure_kpa", -1.0)
        t_sat_spec = self.get_float("sat_temperature_c", -1.0)
        target_ss = self.get_float("supersaturation", 1.15)
        target_ds_pct = self.get_float("total_solids_pct", 92.0)
        t_mc_spec = self.get_float("massecuite_out_temp_c", -999.0)
        cond_drop = self.get_float("condensate_drop_k", 2.0)
        heat_loss_pct = self.get_float("heat_loss_pct", 2.0)
        heat_eff = max(0.01, 1.0 - heat_loss_pct / 100.0)
        color_rise = self.get_float("color_rise", 0.0)

        # Solubility coefficients (inherits from feed unless explicitly overridden §A11)
        a_coef = self.get_float("sol_coef_a", feed_in.sol_coef_a)
        b_coef = self.get_float("sol_coef_b", feed_in.sol_coef_b)
        c_coef = self.get_float("sol_coef_c", feed_in.sol_coef_c)

        # 1. Vacuum Vapor Pressure & Temperature
        if p_vap > 0.0:
            t_vap = water_sat_temp_c(p_vap)
        elif t_sat_spec > 0.0:
            t_vap = t_sat_spec
            p_vap = water_sat_pressure_kpa(t_sat_spec)
        else:
            # Typical pan vacuum ~ 18 kPa (approx 57.8°C saturation)
            p_vap = 18.0
            t_vap = water_sat_temp_c(p_vap)

        m_feed = feed_in.mass_flow_kgh
        ds_feed = feed_in.ds_fraction
        purity_feed = feed_in.purity_fraction

        if m_feed <= 1e-9 or ds_feed <= 1e-6:
            out_streams = {ofid: Stream(pressure_kpa=p_vap) for ofid in outlet_flow_ids}
            return StationResult(outlet_streams=out_streams, warnings=warnings)

        # 2. Massecuite Mass and Evaporation
        target_ds = min(0.98, max(ds_feed, target_ds_pct / 100.0))
        m_mc = m_feed * (ds_feed / target_ds)
        m_evap = max(0.0, m_feed - m_mc)

        # 3. Boiling Point Elevation (BPE) and Boiling Temperature
        bpe_val = bpe_celsius(target_ds, purity_feed, p_vap)
        t_boil = t_vap + bpe_val
        if t_mc_spec > -200.0:
            t_boil = t_mc_spec

        # 4. Authentic Crystal Yield via Vavrinecz Solubility & Equilibrium
        cryst_result = crystals_forward(
            ds_mc=target_ds,
            pu_mc=purity_feed,
            temp_c=t_boil,
            ss=target_ss,
            a=a_coef,
            b=b_coef,
            c=c_coef,
        )
        crystal_frac = max(0.0, cryst_result["crystal_frac"])
        ds_ml = cryst_result["ds_ml"]
        purity_ml = cryst_result["pu_ml"]
        m_crystals = m_mc * crystal_frac

        # 5. Formulate Massecuite Stream
        # Total sucrose in massecuite = target_ds * purity_feed
        # Dissolved sucrose = total_sucrose - crystal_frac
        tot_sucrose_frac = target_ds * purity_feed
        dissolved_sucrose_frac = max(0.0, tot_sucrose_frac - crystal_frac)

        # Non-sucrose components scaled to massecuite
        scale_mc = m_feed / m_mc
        water_frac = max(0.0, (feed_in.water * m_feed - m_evap) / m_mc)

        mc_stream = Stream(
            mass_flow_kgh=m_mc,
            temperature_c=t_boil,
            pressure_kpa=p_vap,
            water=water_frac,
            dissolved_sucrose=dissolved_sucrose_frac,
            non_sucrose_1=feed_in.non_sucrose_1 * scale_mc,
            non_sucrose_2=feed_in.non_sucrose_2 * scale_mc,
            component_5=feed_in.component_5 * scale_mc,
            sucrose_crystals=crystal_frac,
            fiber_isns=feed_in.fiber_isns * scale_mc,
            cao=feed_in.cao * scale_mc,
            caco3=feed_in.caco3 * scale_mc,
            component_10=feed_in.component_10 * scale_mc,
            water_vapor=0.0,
            co2=0.0,
            nh3=0.0,
            non_condensable=0.0,
            component_15=0.0,
            color_icu=feed_in.color_icu + color_rise,
            sol_coef_a=a_coef,
            sol_coef_b=b_coef,
            sol_coef_c=c_coef,
        ).normalize()

        # 6. Energy Balance & Steam Demand (RULES_v5.md §A7: Pan Steam is ALWAYS REQUIRED)
        h_feed = feed_in.enthalpy_kjkg
        h_vap = water_enthalpy_kJkg(t_vap, p_vap, quality=1.0)
        h_mc = mc_stream.enthalpy_kjkg

        # Exothermic heat of crystallization releases heat
        q_cryst_heat_kjh = m_crystals * heat_of_crystallization_kJkg()

        # Evaporation heat load
        q_boil_kjh = (m_evap * h_vap + m_mc * h_mc) - (m_feed * h_feed) - q_cryst_heat_kjh
        q_steam_req_kjh = max(0.0, q_boil_kjh / heat_eff)

        # Steam consumption
        p_steam = steam_in.pressure_kpa if steam_in else 160.0
        t_sat_steam = water_sat_temp_c(p_steam)
        t_cond = max(20.0, t_sat_steam - cond_drop)
        h_steam_in = steam_in.enthalpy_kjkg if steam_in else water_enthalpy_kJkg(t_sat_steam, p_steam, quality=1.0)
        h_cond_out = water_enthalpy_kJkg(t_cond, p_steam, quality=0.0)
        latent = max(500.0, h_steam_in - h_cond_out)

        m_steam = q_steam_req_kjh / latent
        if steam_id:
            required_inlets[steam_id] = m_steam

        # 7. Formulate Vapor & Condensate Outlets
        vapor_stream = Stream(
            mass_flow_kgh=m_evap,
            temperature_c=t_vap,
            pressure_kpa=p_vap,
            water=0.0,
            water_vapor=1.0,
            dissolved_sucrose=0.0,
            non_sucrose_1=0.0,
            non_sucrose_2=0.0,
            sucrose_crystals=0.0,
            color_icu=0.0,
        ).normalize()

        cond_stream = Stream(
            mass_flow_kgh=m_steam,
            temperature_c=t_cond,
            pressure_kpa=p_steam,
            water=1.0,
            water_vapor=0.0,
        ).normalize()

        outlet_streams = {}
        if len(outlet_flow_ids) == 1:
            outlet_streams[outlet_flow_ids[0]] = mc_stream
        elif len(outlet_flow_ids) == 2:
            outlet_streams[outlet_flow_ids[0]] = mc_stream
            outlet_streams[outlet_flow_ids[1]] = vapor_stream
        elif len(outlet_flow_ids) >= 3:
            outlet_streams[outlet_flow_ids[0]] = mc_stream
            outlet_streams[outlet_flow_ids[1]] = vapor_stream
            outlet_streams[outlet_flow_ids[2]] = cond_stream
            for ofid in outlet_flow_ids[3:]:
                outlet_streams[ofid] = Stream(pressure_kpa=p_vap)

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "massecuite_flow_kgh": round(m_mc, 2),
                "massecuite_brix_pct": round(mc_stream.ds_pct, 2),
                "massecuite_purity_pct": round(mc_stream.purity_pct, 2),
                "crystal_content_pct": round(mc_stream.crystal_pct, 2),
                "crystals_produced_kgh": round(m_crystals, 2),
                "mother_liquor_brix_pct": round(ds_ml * 100.0, 2),
                "mother_liquor_purity_pct": round(purity_ml * 100.0, 2),
                "vapor_generated_kgh": round(m_evap, 2),
                "boiling_temp_c": round(t_boil, 2),
                "bpe_c": round(bpe_val, 2),
                "steam_consumed_kgh": round(m_steam, 2),
                "heat_duty_kw": round(q_boil_kjh / 3600.0, 2),
            },
            warnings=warnings,
            required_inlet_flows=required_inlets,
        )
