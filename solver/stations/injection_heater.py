"""
solver/stations/injection_heater.py
Purity for Sugar — Injection Heater Station Model

Rules:
  - Direct injection of heating steam into process juice
  - 100% condensation of steam into the process stream (direct contact)
  - Dilution: steam condensed becomes liquid water in process stream
  - If temperature_out_c or temperature_rise_k specified, steam is calculated as required flow
  - Crystals may dissolve if undersaturated after heating (RULES_v5.md §A9)
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream, mix_streams


class InjectionHeaterStation(BaseStation):
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
                warnings=["Injection heater has no inlet flows."],
            )

        proc_id = inlet_flow_ids[0]
        proc_in = inlet_streams.get(proc_id, Stream()).copy()

        steam_id = inlet_flow_ids[1] if len(inlet_flow_ids) > 1 else None
        steam_in = inlet_streams.get(steam_id, Stream()).copy() if steam_id else None

        t_out_spec = self.get_float("temperature_out_c", -999.0)
        t_rise_spec = self.get_float("temperature_rise_k", -999.0)
        heat_loss_pct = self.get_float("heat_loss_pct", 0.0)
        heat_eff = max(0.01, 1.0 - heat_loss_pct / 100.0)

        # Target outlet temp
        t_target = proc_in.temperature_c
        if t_out_spec > -200.0:
            t_target = t_out_spec
        elif t_rise_spec > -200.0:
            t_target = proc_in.temperature_c + t_rise_spec

        # Calculate required steam if target temperature is specified
        if steam_id and t_target > proc_in.temperature_c and proc_in.mass_flow_kgh > 0:
            # Q_cold = m_proc * Cp * (t_target - t_in)
            # Latent heat of steam ~ 2200 kJ/kg
            cp_proc = 4.0
            q_cold = proc_in.mass_flow_kgh * cp_proc * (t_target - proc_in.temperature_c)
            h_steam = steam_in.enthalpy_kjkg if steam_in else 2675.0
            # Saturated liquid enthalpy at t_target ~ 4.18 * t_target
            h_cond = 4.18 * t_target
            delta_h = max(500.0, (h_steam - h_cond) * heat_eff)
            req_steam = max(0.0, q_cold / delta_h)
            required_inlets[steam_id] = req_steam
            if steam_in:
                steam_in.mass_flow_kgh = req_steam

        # Mix process fluid and steam
        active_inlets = [proc_in]
        if steam_in:
            # In direct injection heater, the steam condenses into liquid water
            steam_liquid = steam_in.copy()
            steam_liquid.water = 1.0
            steam_liquid.water_vapor = 0.0
            steam_liquid.normalize()
            active_inlets.append(steam_liquid)

        mixed = mix_streams(active_inlets, pressure_mode="minimum")

        if t_target > -200.0 and (t_out_spec > -200.0 or t_rise_spec > -200.0):
            mixed.temperature_c = t_target

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
                "ds_pct": mixed.ds_pct,
                "temperature_c": mixed.temperature_c,
                "steam_injected_kgh": steam_in.mass_flow_kgh if steam_in else 0.0,
            },
            warnings=warnings,
            required_inlet_flows=required_inlets,
        )
