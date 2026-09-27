"""
solver/stations/flash_tank.py
Purity for Sugar — Flash Tank Station Model

Rules:
  - Flashes hot pressurized liquid to lower pressure
  - Vapor output carries water vapor at vessel pressure/temperature
  - Liquid output carries all non-volatile dry substance
  - Energy conservation: m_in * h_in = m_vap * h_vap + m_liq * h_liq
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream, mix_streams
from engine.fluids import water_sat_pressure_kpa, water_sat_temp_c, water_enthalpy_kJkg
from engine.enthalpy import flow_enthalpy_kJkg


class FlashTankStation(BaseStation):
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
                warnings=["Flash tank has no inlet flows."],
            )

        inlets = [inlet_streams[fid] for fid in inlet_flow_ids if fid in inlet_streams]
        in_stream = mix_streams(inlets)

        m_in = in_stream.mass_flow_kgh
        if m_in <= 1e-9:
            return StationResult(
                outlet_streams={ofid: Stream() for ofid in outlet_flow_ids},
                calculated_properties={"mass_flow_in": 0.0},
            )

        # Vessel pressure
        p_tank = self.get_float("vapor_pressure_kpa", -1.0)
        t_sat = self.get_float("sat_temperature_c", -1.0)

        if p_tank > 0.0:
            t_boil = water_sat_temp_c(p_tank)
        elif t_sat > 0.0:
            t_boil = t_sat
            p_tank = water_sat_pressure_kpa(t_sat)
        else:
            p_tank = atmospheric_p_kpa
            t_boil = water_sat_temp_c(p_tank)

        # Check flashing condition: inlet temperature must be above vessel boiling temperature
        h_in = in_stream.enthalpy_kjkg
        h_vap = water_enthalpy_kJkg(t_boil, p_tank, quality=1.0)

        # Flashed liquid enthalpy at t_boil
        # Approximate flashed liquid with reduced water content
        if in_stream.temperature_c > t_boil:
            # Flashing occurs
            # Iterative energy balance to find m_vap
            m_vap = 0.0
            for _ in range(10):
                m_liq = max(1e-6, m_in - m_vap)
                # Composition of liquid
                water_liq = max(0.0, in_stream.mass_flow_kgh * in_stream.water - m_vap) / m_liq
                ds_liq = min(1.0, (in_stream.ds_fraction * m_in) / m_liq)
                liq_fractions = {
                    "water": water_liq,
                    "sucrose": (in_stream.dissolved_sucrose * m_in) / m_liq,
                    "ns1": (in_stream.non_sucrose_1 * m_in) / m_liq,
                    "ns2": (in_stream.non_sucrose_2 * m_in) / m_liq,
                    "crystals": (in_stream.sucrose_crystals * m_in) / m_liq,
                    "fiber": (in_stream.fiber_isns * m_in) / m_liq,
                }
                h_liq = flow_enthalpy_kJkg(liq_fractions, t_boil, p_tank)
                latent = max(100.0, h_vap - h_liq)
                new_m_vap = max(0.0, min(m_in * in_stream.water, m_in * (h_in - h_liq) / latent))
                if abs(new_m_vap - m_vap) < 1e-4:
                    m_vap = new_m_vap
                    break
                m_vap = new_m_vap
        else:
            # Subcooled feed, no flash vapor generated
            m_vap = 0.0
            m_liq = m_in

        m_liq = max(0.0, m_in - m_vap)

        # 1. Vapor stream (100% steam at t_boil, p_tank)
        vapor_stream = Stream(
            mass_flow_kgh=m_vap,
            temperature_c=t_boil,
            pressure_kpa=p_tank,
            water=0.0,
            water_vapor=1.0,
            dissolved_sucrose=0.0,
            non_sucrose_1=0.0,
            non_sucrose_2=0.0,
            sucrose_crystals=0.0,
            fiber_isns=0.0,
            color_icu=0.0,
        ).normalize()

        # 2. Liquid stream (concentrated liquid at t_boil, p_tank)
        if m_liq > 1e-6:
            scale_liq = m_in / m_liq
            liq_stream = Stream(
                mass_flow_kgh=m_liq,
                temperature_c=t_boil,
                pressure_kpa=p_tank,
                water=max(0.0, (in_stream.water * m_in - m_vap) / m_liq),
                dissolved_sucrose=in_stream.dissolved_sucrose * scale_liq,
                non_sucrose_1=in_stream.non_sucrose_1 * scale_liq,
                non_sucrose_2=in_stream.non_sucrose_2 * scale_liq,
                component_5=in_stream.component_5 * scale_liq,
                sucrose_crystals=in_stream.sucrose_crystals * scale_liq,
                fiber_isns=in_stream.fiber_isns * scale_liq,
                cao=in_stream.cao * scale_liq,
                caco3=in_stream.caco3 * scale_liq,
                component_10=in_stream.component_10 * scale_liq,
                water_vapor=0.0,
                co2=0.0,
                nh3=0.0,
                non_condensable=0.0,
                component_15=0.0,
                color_icu=in_stream.color_icu,
                sol_coef_a=in_stream.sol_coef_a,
                sol_coef_b=in_stream.sol_coef_b,
                sol_coef_c=in_stream.sol_coef_c,
            ).normalize()
        else:
            liq_stream = Stream(mass_flow_kgh=0.0, temperature_c=t_boil, pressure_kpa=p_tank)

        outlet_streams = {}
        if len(outlet_flow_ids) == 1:
            # Only 1 outlet connected: return liquid if m_liq > 0, else vapor
            outlet_streams[outlet_flow_ids[0]] = liq_stream if m_liq > 0 else vapor_stream
        elif len(outlet_flow_ids) >= 2:
            # Outlet 0 is liquid bottom; Outlet 1 is vapor top
            outlet_streams[outlet_flow_ids[0]] = liq_stream
            outlet_streams[outlet_flow_ids[1]] = vapor_stream
            # Any remaining outlets get 0 flow
            for ofid in outlet_flow_ids[2:]:
                outlet_streams[ofid] = Stream(mass_flow_kgh=0.0, temperature_c=t_boil, pressure_kpa=p_tank)

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "flash_temp_c": t_boil,
                "tank_pressure_kpa": p_tank,
                "vapor_generated_kgh": m_vap,
                "liquid_out_kgh": m_liq,
                "liquid_ds_pct": liq_stream.ds_pct,
            },
            warnings=warnings,
        )
