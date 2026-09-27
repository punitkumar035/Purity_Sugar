"""
solver/stations/evaporator.py
Purity for Sugar — Evaporator Effect Station Model

Rules:
  - Juice feed concentrated by boiling under vacuum or pressure
  - Boiling Point Elevation (BPE) calculated via Bubnik-Kadlec / KBD model (RULES_v5.md §B6)
  - Motive steam conditionally required when total_solids_pct is specified (RULES_v5.md §A7)
  - Evaporator vapor out and condensate out CANNOT be required (RULES_v5.md §A7)
  - Crystals count maintained: no growth, no dissolution (RULES_v5.md §A9)
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream
from engine.fluids import water_sat_temp_c, water_sat_pressure_kpa, water_enthalpy_kJkg
from engine.bpe import bpe_celsius
from engine.enthalpy import flow_enthalpy_kJkg


class EvaporatorStation(BaseStation):
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
                warnings=["Evaporator has no inlet flows."],
            )

        # Port 0: Juice feed
        juice_id = inlet_flow_ids[0]
        juice_in = inlet_streams.get(juice_id, Stream()).copy()

        # Port 1: Heating steam / vapor
        steam_id = inlet_flow_ids[1] if len(inlet_flow_ids) > 1 else None
        steam_in = inlet_streams.get(steam_id, Stream()).copy() if steam_id else None

        # Properties
        p_vap = self.get_float("vapor_pressure_kpa", -1.0)
        t_sat_spec = self.get_float("sat_temperature_c", -1.0)
        target_ds_pct = self.get_float("total_solids_pct", -1.0)
        bpe_factor = self.get_float("bpe_factor", 1.0)
        cond_drop = self.get_float("condensate_drop_k", 0.0)
        heat_loss_pct = self.get_float("heat_loss_pct", 1.5)
        heat_eff = max(0.01, 1.0 - heat_loss_pct / 100.0)
        color_rise = self.get_float("color_rise", 0.0)

        # 1. Vapor Pressure & Saturation Temperature
        if p_vap > 0.0:
            t_vap = water_sat_temp_c(p_vap)
        elif t_sat_spec > 0.0:
            t_vap = t_sat_spec
            p_vap = water_sat_pressure_kpa(t_sat_spec)
        else:
            p_vap = atmospheric_p_kpa
            t_vap = water_sat_temp_c(p_vap)

        m_juice = juice_in.mass_flow_kgh
        ds_in = juice_in.ds_fraction
        purity_in = juice_in.purity_fraction

        if m_juice <= 1e-9 or ds_in <= 1e-6:
            # Empty juice feed
            out_streams = {ofid: Stream(temperature_c=t_vap, pressure_kpa=p_vap) for ofid in outlet_flow_ids}
            return StationResult(outlet_streams=out_streams, warnings=warnings)

        # 2. Target Concentration & Evaporation
        if target_ds_pct > 0.0:
            target_ds = min(0.95, max(ds_in, target_ds_pct / 100.0))
            m_syrup = m_juice * (ds_in / target_ds)
            m_evap = max(0.0, m_juice - m_syrup)
        else:
            # Target DS not specified; if steam is supplied, calculate evaporation from steam heat
            if steam_in and steam_in.mass_flow_kgh > 0:
                p_s = steam_in.pressure_kpa
                t_s = water_sat_temp_c(p_s)
                h_s_in = steam_in.enthalpy_kjkg
                h_c_out = water_enthalpy_kJkg(max(20.0, t_s - cond_drop), p_s, quality=0.0)
                q_steam = steam_in.mass_flow_kgh * max(500.0, h_s_in - h_c_out) * heat_eff
                latent_vap = 2250.0  # approximate latent heat of water evaporation
                m_evap = min(m_juice * (1.0 - ds_in), q_steam / latent_vap)
                m_syrup = max(1e-6, m_juice - m_evap)
                target_ds = min(0.95, (m_juice * ds_in) / m_syrup)
            else:
                m_evap = 0.0
                m_syrup = m_juice
                target_ds = ds_in

        # 3. Boiling Point Elevation (BPE)
        bpe_val = bpe_factor * bpe_celsius(target_ds, purity_in, p_vap)
        t_boil = t_vap + bpe_val

        # 4. Energy Balance & Steam Demand (RULES_v5.md §A7)
        h_juice = juice_in.enthalpy_kjkg
        h_vap = water_enthalpy_kJkg(t_vap, p_vap, quality=1.0)

        # Syrup stream
        scale_syrup = m_juice / m_syrup
        syrup_stream = Stream(
            mass_flow_kgh=m_syrup,
            temperature_c=t_boil,
            pressure_kpa=p_vap,
            water=max(0.0, (juice_in.water * m_juice - m_evap) / m_syrup),
            dissolved_sucrose=juice_in.dissolved_sucrose * scale_syrup,
            non_sucrose_1=juice_in.non_sucrose_1 * scale_syrup,
            non_sucrose_2=juice_in.non_sucrose_2 * scale_syrup,
            component_5=juice_in.component_5 * scale_syrup,
            sucrose_crystals=juice_in.sucrose_crystals * scale_syrup,  # crystals maintained §A9
            fiber_isns=juice_in.fiber_isns * scale_syrup,
            cao=juice_in.cao * scale_syrup,
            caco3=juice_in.caco3 * scale_syrup,
            component_10=juice_in.component_10 * scale_syrup,
            water_vapor=0.0,
            co2=0.0,
            nh3=0.0,
            non_condensable=0.0,
            component_15=0.0,
            color_icu=juice_in.color_icu + color_rise,
            sol_coef_a=juice_in.sol_coef_a,
            sol_coef_b=juice_in.sol_coef_b,
            sol_coef_c=juice_in.sol_coef_c,
        ).normalize()

        h_syrup = syrup_stream.enthalpy_kjkg
        q_evap_kjh = (m_evap * h_vap + m_syrup * h_syrup) - (m_juice * h_juice)
        q_steam_req_kjh = max(0.0, q_evap_kjh / heat_eff)

        # Steam calculation
        m_steam = 0.0
        t_cond = 100.0
        p_steam = steam_in.pressure_kpa if steam_in else 150.0

        if steam_id:
            t_sat_steam = water_sat_temp_c(p_steam)
            t_cond = max(20.0, t_sat_steam - cond_drop)
            h_steam_in = steam_in.enthalpy_kjkg if steam_in else water_enthalpy_kJkg(t_sat_steam, p_steam, quality=1.0)
            h_cond_out = water_enthalpy_kJkg(t_cond, p_steam, quality=0.0)
            latent = max(500.0, h_steam_in - h_cond_out)

            if target_ds_pct > 0.0:
                # Target solids specified -> calculate required steam flow
                m_steam = q_steam_req_kjh / latent
                required_inlets[steam_id] = m_steam
            else:
                m_steam = steam_in.mass_flow_kgh

        # 5. Outlets Configuration:
        # Port 0 = Concentrated syrup
        # Port 1 = Generated vapor
        # Port 2 = Heating condensate
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
            fiber_isns=0.0,
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
            outlet_streams[outlet_flow_ids[0]] = syrup_stream
        elif len(outlet_flow_ids) == 2:
            outlet_streams[outlet_flow_ids[0]] = syrup_stream
            outlet_streams[outlet_flow_ids[1]] = vapor_stream
        elif len(outlet_flow_ids) >= 3:
            outlet_streams[outlet_flow_ids[0]] = syrup_stream
            outlet_streams[outlet_flow_ids[1]] = vapor_stream
            outlet_streams[outlet_flow_ids[2]] = cond_stream
            for ofid in outlet_flow_ids[3:]:
                outlet_streams[ofid] = Stream(pressure_kpa=p_vap)

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "syrup_flow_kgh": round(m_syrup, 2),
                "syrup_brix_pct": round(syrup_stream.ds_pct, 2),
                "vapor_generated_kgh": round(m_evap, 2),
                "vapor_temp_c": round(t_vap, 2),
                "bpe_c": round(bpe_val, 2),
                "boiling_temp_c": round(t_boil, 2),
                "evaporation_heat_duty_kw": round(q_evap_kjh / 3600.0, 2),
                "steam_consumed_kgh": round(m_steam, 2),
            },
            warnings=warnings,
            required_inlet_flows=required_inlets,
        )
