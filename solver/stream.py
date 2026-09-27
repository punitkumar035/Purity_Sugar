"""
solver/stream.py
Purity for Sugar — 15-Component Process Stream Representation

Enforces strict SI units internally:
  - Mass flow  : kg/h
  - Temperature: °C
  - Pressure   : kPa absolute
  - Fractions  : 0.0 to 1.0 (weight fractions)
  - Enthalpy   : kJ/kg
  - Density    : kg/m³

Governed by:
  - RULES_v5.md §A6 (15-Component Flow Stream Model)
  - RULES_v5.md §B7 (Enthalpy) & §B8 (Density)
  - Sugar's Help Book Theory & Component Balances
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Mapping

from engine.solubility import supersaturation, saturation_coefficient
from engine.enthalpy import flow_enthalpy_kJkg
from engine.density import syrup_density_kgm3, massecuite_density_kgm3


@dataclass
class Stream:
    """
    Standard process stream with 15 chemical/physical components and thermodynamic states.
    All component quantities stored as normalized mass fractions summing to 1.0 (or 0.0 if empty).
    """
    # Flow and state
    mass_flow_kgh: float = 0.0
    temperature_c: float = 20.0
    pressure_kpa: float = 101.325

    # 15 Chemical Components (fractions 0.0 to 1.0)
    # Liquid phase
    water: float = 1.0
    dissolved_sucrose: float = 0.0
    non_sucrose_1: float = 0.0
    non_sucrose_2: float = 0.0
    component_5: float = 0.0

    # Solid phase
    sucrose_crystals: float = 0.0
    fiber_isns: float = 0.0
    cao: float = 0.0
    caco3: float = 0.0
    component_10: float = 0.0

    # Gas phase
    water_vapor: float = 0.0
    co2: float = 0.0
    nh3: float = 0.0
    non_condensable: float = 0.0
    component_15: float = 0.0

    # Attributes
    color_icu: float = 0.0
    sol_coef_a: float = 0.04
    sol_coef_b: float = 0.71
    sol_coef_c: float = -2.1

    def copy(self) -> Stream:
        return Stream(
            mass_flow_kgh=self.mass_flow_kgh,
            temperature_c=self.temperature_c,
            pressure_kpa=self.pressure_kpa,
            water=self.water,
            dissolved_sucrose=self.dissolved_sucrose,
            non_sucrose_1=self.non_sucrose_1,
            non_sucrose_2=self.non_sucrose_2,
            component_5=self.component_5,
            sucrose_crystals=self.sucrose_crystals,
            fiber_isns=self.fiber_isns,
            cao=self.cao,
            caco3=self.caco3,
            component_10=self.component_10,
            water_vapor=self.water_vapor,
            co2=self.co2,
            nh3=self.nh3,
            non_condensable=self.non_condensable,
            component_15=self.component_15,
            color_icu=self.color_icu,
            sol_coef_a=self.sol_coef_a,
            sol_coef_b=self.sol_coef_b,
            sol_coef_c=self.sol_coef_c,
        )

    def normalize(self) -> Stream:
        """Normalizes component fractions so their sum is strictly 1.0 (unless all 0)."""
        tot = (
            self.water
            + self.dissolved_sucrose
            + self.non_sucrose_1
            + self.non_sucrose_2
            + self.component_5
            + self.sucrose_crystals
            + self.fiber_isns
            + self.cao
            + self.caco3
            + self.component_10
            + self.water_vapor
            + self.co2
            + self.nh3
            + self.non_condensable
            + self.component_15
        )
        if tot > 1e-12:
            scale = 1.0 / tot
            self.water *= scale
            self.dissolved_sucrose *= scale
            self.non_sucrose_1 *= scale
            self.non_sucrose_2 *= scale
            self.component_5 *= scale
            self.sucrose_crystals *= scale
            self.fiber_isns *= scale
            self.cao *= scale
            self.caco3 *= scale
            self.component_10 *= scale
            self.water_vapor *= scale
            self.co2 *= scale
            self.nh3 *= scale
            self.non_condensable *= scale
            self.component_15 *= scale
        return self

    @property
    def tdm_fraction(self) -> float:
        """Total dry matter fraction (1 - water - water_vapor)."""
        return max(0.0, min(1.0, 1.0 - self.water - self.water_vapor))

    @property
    def tdm_pct(self) -> float:
        return self.tdm_fraction * 100.0

    @property
    def ds_fraction(self) -> float:
        """
        Soluble dry substance plus crystal sucrose fraction.
        DS = dissolved_sucrose + non_sucrose_1 + non_sucrose_2 + sucrose_crystals (+ component_5 if soluble).
        """
        val = (
            self.dissolved_sucrose
            + self.non_sucrose_1
            + self.non_sucrose_2
            + self.sucrose_crystals
        )
        return max(0.0, min(1.0, val))

    @property
    def ds_pct(self) -> float:
        return self.ds_fraction * 100.0

    @property
    def dissolved_ds_fraction(self) -> float:
        """Soluble dry substance in mother liquor / syrup (excluding crystals)."""
        val = self.dissolved_sucrose + self.non_sucrose_1 + self.non_sucrose_2
        return max(0.0, min(1.0, val))

    @property
    def ml_ds_fraction(self) -> float:
        """Mother liquor dry substance fraction: DS_ml = DS_dissolved / (DS_dissolved + Water)."""
        denom = self.dissolved_ds_fraction + self.water
        if denom > 1e-9:
            return max(0.0, min(1.0, self.dissolved_ds_fraction / denom))
        return 0.0

    @property
    def purity_fraction(self) -> float:
        """Purity fraction = Total Sucrose / DS."""
        ds = self.ds_fraction
        if ds > 1e-9:
            total_suc = self.dissolved_sucrose + self.sucrose_crystals
            return max(0.0, min(1.0, total_suc / ds))
        return 0.0

    @property
    def purity_pct(self) -> float:
        return self.purity_fraction * 100.0

    @property
    def ml_purity_fraction(self) -> float:
        """Mother liquor purity fraction = Dissolved Sucrose / Dissolved DS."""
        dds = self.dissolved_ds_fraction
        if dds > 1e-9:
            return max(0.0, min(1.0, self.dissolved_sucrose / dds))
        return 0.0

    @property
    def ml_purity_pct(self) -> float:
        return self.ml_purity_fraction * 100.0

    @property
    def crystal_fraction(self) -> float:
        return max(0.0, min(1.0, self.sucrose_crystals))

    @property
    def crystal_pct(self) -> float:
        return self.crystal_fraction * 100.0

    @property
    def sugar_pct(self) -> float:
        """Total sugar (dissolved + crystal) percent."""
        return (self.dissolved_sucrose + self.sucrose_crystals) * 100.0

    @property
    def isns_pct(self) -> float:
        return self.fiber_isns * 100.0

    @property
    def gas_pct(self) -> float:
        return (
            self.water_vapor
            + self.co2
            + self.nh3
            + self.non_condensable
            + self.component_15
        ) * 100.0

    @property
    def nsw(self) -> float:
        """Non-sucrose to water ratio: NSW = NonSucrose1 / Water."""
        if self.water > 1e-9:
            return self.non_sucrose_1 / self.water
        return 0.0

    @property
    def supersaturation(self) -> float:
        """Supersaturation ratio of the mother liquor / liquid phase."""
        if self.water <= 1e-9 or self.dissolved_sucrose <= 1e-9:
            return 0.0
        ml_ds = self.ml_ds_fraction
        ml_pur = self.ml_purity_fraction
        if ml_ds <= 1e-9 or ml_pur <= 1e-9:
            return 0.0
        try:
            return supersaturation(
                ds_frac=ml_ds,
                purity_frac=ml_pur,
                temp_c=self.temperature_c,
                a=self.sol_coef_a,
                b=self.sol_coef_b,
                c=self.sol_coef_c,
            )
        except Exception:
            return 0.0

    @property
    def enthalpy_kjkg(self) -> float:
        """Calculates specific enthalpy in kJ/kg with 0°C liquid water reference."""
        frac_map = {
            "water": self.water,
            "sucrose": self.dissolved_sucrose,
            "ns1": self.non_sucrose_1,
            "ns2": self.non_sucrose_2,
            "crystals": self.sucrose_crystals,
            "fiber": self.fiber_isns,
            "cao": self.cao,
            "caco3": self.caco3,
            "steamVapour": self.water_vapor,
            "co2": self.co2,
            "ammonia": self.nh3,
            "ethanolL": self.component_5,
            "ethanolG": 0.0,
        }
        return flow_enthalpy_kJkg(frac_map, self.temperature_c, self.pressure_kpa)

    @property
    def total_enthalpy_flow_kjh(self) -> float:
        """Total enthalpy flow rate in kJ/h: H_dot = m_dot * h."""
        return self.mass_flow_kgh * self.enthalpy_kjkg

    @property
    def density_kgm3(self) -> float:
        """Calculates density in kg/m3 for syrup or two-phase massecuite."""
        if self.gas_pct > 50.0:
            # Gas / steam density estimate using ideal gas law at low-to-mid pressure
            p_pa = self.pressure_kpa * 1000.0
            t_k = self.temperature_c + 273.15
            # Mw of steam = 0.018015 kg/mol
            r_spec = 8314.46 / 18.015  # J/(kg K)
            return max(0.1, p_pa / (r_spec * t_k))

        if self.crystal_fraction > 0.005:
            # Massecuite
            return massecuite_density_kgm3(
                ds_mc=self.ds_fraction,
                pu_mc=self.purity_fraction,
                crystal_frac=self.crystal_fraction,
                temp_c=self.temperature_c,
            )
        else:
            # Liquid syrup / water
            return syrup_density_kgm3(self.ds_fraction, self.temperature_c)

    @property
    def fluid_type(self) -> str:
        """Categorizes fluid type for display and styling."""
        if self.gas_pct > 50.0:
            if self.water_vapor > 0.5:
                return "steam"
            return "gas"
        if self.crystal_fraction > 0.005:
            return "massecuite"
        if self.ds_fraction > 0.60:
            return "heavy_syrup"
        if self.ds_fraction > 0.10:
            return "syrup"
        if self.ds_fraction > 0.001:
            return "thin_juice"
        return "water"

    def to_wire_dict(self, stream_id: str) -> Dict[str, Any]:
        """Converts stream state into the JSON dictionary expected by Visio and frontend."""
        return {
            "id": stream_id,
            "mass_flow_kgh": round(self.mass_flow_kgh, 4),
            "temperature_c": round(self.temperature_c, 3),
            "pressure_kpa": round(self.pressure_kpa, 3),
            "tdm_pct": round(self.tdm_pct, 4),
            "sugar_pct": round(self.sugar_pct, 4),
            "ds_pct": round(self.ds_pct, 4),
            "purity_pct": round(self.purity_pct, 4),
            "crystal_pct": round(self.crystal_pct, 4),
            "isns_pct": round(self.isns_pct, 4),
            "gas_pct": round(self.gas_pct, 4),
            "color_icu": round(self.color_icu, 1),
            "enthalpy_kjkg": round(self.enthalpy_kjkg, 3),
            "density_kgm3": round(self.density_kgm3, 2),
            "fluid_type": self.fluid_type,
            "water": round(self.water, 6),
            "dissolved_sucrose": round(self.dissolved_sucrose, 6),
            "non_sucrose_1": round(self.non_sucrose_1, 6),
            "non_sucrose_2": round(self.non_sucrose_2, 6),
            "component_5": round(self.component_5, 6),
            "sucrose_crystals": round(self.sucrose_crystals, 6),
            "fiber_isns": round(self.fiber_isns, 6),
            "cao": round(self.cao, 6),
            "caco3": round(self.caco3, 6),
            "component_10": round(self.component_10, 6),
            "water_vapor": round(self.water_vapor, 6),
            "co2": round(self.co2, 6),
            "nh3": round(self.nh3, 6),
            "non_condensable": round(self.non_condensable, 6),
            "component_15": round(self.component_15, 6),
            "sol_coef_a": round(self.sol_coef_a, 4),
            "sol_coef_b": round(self.sol_coef_b, 4),
            "sol_coef_c": round(self.sol_coef_c, 4),
        }

    @classmethod
    def from_initial_state(
        cls, state: Mapping[str, Any], default_p_kpa: float = 101.325
    ) -> Stream:
        """Constructs a Stream from the initial_state dictionary sent by Visio or Web App."""
        mass_flow = float(state.get("mass_flow_kgh", 0.0) or 0.0)
        temp_c = float(state.get("temperature_c", 20.0) or 20.0)
        p_kpa = float(state.get("pressure_kpa", default_p_kpa) or default_p_kpa)
        if p_kpa <= 0.0:
            p_kpa = default_p_kpa

        # Check if individual 15 components are populated
        w = float(state.get("water", 0.0) or 0.0)
        dsuc = float(state.get("dissolved_sucrose", 0.0) or 0.0)
        ns1 = float(state.get("non_sucrose_1", 0.0) or 0.0)
        ns2 = float(state.get("non_sucrose_2", 0.0) or 0.0)
        c5 = float(state.get("component_5", 0.0) or 0.0)
        cryst = float(state.get("sucrose_crystals", 0.0) or 0.0)
        fib = float(state.get("fiber_isns", 0.0) or 0.0)
        cao_val = float(state.get("cao", 0.0) or 0.0)
        caco3_val = float(state.get("caco3", 0.0) or 0.0)
        c10 = float(state.get("component_10", 0.0) or 0.0)
        vap = float(state.get("water_vapor", 0.0) or 0.0)
        co2_val = float(state.get("co2", 0.0) or 0.0)
        nh3_val = float(state.get("nh3", 0.0) or 0.0)
        nc = float(state.get("non_condensable", 0.0) or 0.0)
        c15 = float(state.get("component_15", 0.0) or 0.0)

        tot_components = (
            w + dsuc + ns1 + ns2 + c5 + cryst + fib + cao_val + caco3_val + c10 + vap + co2_val + nh3_val + nc + c15
        )

        # If components were not entered individually, construct them from ds_pct, purity_pct, crystal_pct
        if tot_components <= 1e-6:
            ds_pct = float(state.get("ds_pct", 0.0) or 0.0)
            purity_pct = float(state.get("purity_pct", 0.0) or 0.0)
            crystal_pct = float(state.get("crystal_pct", 0.0) or 0.0)
            isns_pct = float(state.get("isns_pct", 0.0) or 0.0)
            gas_pct = float(state.get("gas_pct", 0.0) or 0.0)

            if gas_pct > 50.0:
                vap = gas_pct / 100.0
                w = max(0.0, 1.0 - vap)
            else:
                ds_frac = max(0.0, min(1.0, ds_pct / 100.0))
                purity_frac = max(0.0, min(1.0, purity_pct / 100.0))
                cryst_frac = max(0.0, min(ds_frac, crystal_pct / 100.0))
                fib_frac = max(0.0, min(1.0, isns_pct / 100.0))

                total_sucrose = ds_frac * purity_frac
                dissolved_suc = max(0.0, total_sucrose - cryst_frac)
                non_sucrose = max(0.0, ds_frac - total_sucrose)

                # Assign non-sucrose to ns1 and ns2
                ns1 = non_sucrose * 0.8
                ns2 = non_sucrose * 0.2
                dsuc = dissolved_suc
                cryst = cryst_frac
                fib = fib_frac
                w = max(0.0, 1.0 - ds_frac - fib)

        color = float(state.get("color_icu", 0.0) or 0.0)
        a = float(state.get("sol_coef_a", 0.04) or 0.04)
        b = float(state.get("sol_coef_b", 0.71) or 0.71)
        c = float(state.get("sol_coef_c", -2.1) or -2.1)

        st = cls(
            mass_flow_kgh=mass_flow,
            temperature_c=temp_c,
            pressure_kpa=p_kpa,
            water=w,
            dissolved_sucrose=dsuc,
            non_sucrose_1=ns1,
            non_sucrose_2=ns2,
            component_5=c5,
            sucrose_crystals=cryst,
            fiber_isns=fib,
            cao=cao_val,
            caco3=caco3_val,
            component_10=c10,
            water_vapor=vap,
            co2=co2_val,
            nh3=nh3_val,
            non_condensable=nc,
            component_15=c15,
            color_icu=color,
            sol_coef_a=a,
            sol_coef_b=b,
            sol_coef_c=c,
        )
        return st.normalize()


def mix_streams(streams: list[Stream], pressure_mode: str = "minimum") -> Stream:
    """
    Adiabatically and chemically mixes multiple streams into a single composite stream.
    Enforces exact component mass conservation and enthalpy conservation.

    Args:
        streams: List of Stream objects to mix.
        pressure_mode: "minimum" (standard receiver rule), "average", or "maximum".

    Returns:
        New composite Stream object.
    """
    active = [s for s in streams if s.mass_flow_kgh > 1e-9]
    if not active:
        # Return default blank stream with default pressure
        p = min((s.pressure_kpa for s in streams), default=101.325)
        return Stream(mass_flow_kgh=0.0, temperature_c=20.0, pressure_kpa=p)

    total_mass = sum(s.mass_flow_kgh for s in active)
    if total_mass <= 1e-9:
        p = min(s.pressure_kpa for s in active)
        return Stream(mass_flow_kgh=0.0, temperature_c=20.0, pressure_kpa=p)

    if len(active) == 1:
        res = active[0].copy()
        res.mass_flow_kgh = total_mass
        return res

    # 1. Component mass conservation
    comp_mass = {
        "water": sum(s.mass_flow_kgh * s.water for s in active),
        "dissolved_sucrose": sum(s.mass_flow_kgh * s.dissolved_sucrose for s in active),
        "non_sucrose_1": sum(s.mass_flow_kgh * s.non_sucrose_1 for s in active),
        "non_sucrose_2": sum(s.mass_flow_kgh * s.non_sucrose_2 for s in active),
        "component_5": sum(s.mass_flow_kgh * s.component_5 for s in active),
        "sucrose_crystals": sum(s.mass_flow_kgh * s.sucrose_crystals for s in active),
        "fiber_isns": sum(s.mass_flow_kgh * s.fiber_isns for s in active),
        "cao": sum(s.mass_flow_kgh * s.cao for s in active),
        "caco3": sum(s.mass_flow_kgh * s.caco3 for s in active),
        "component_10": sum(s.mass_flow_kgh * s.component_10 for s in active),
        "water_vapor": sum(s.mass_flow_kgh * s.water_vapor for s in active),
        "co2": sum(s.mass_flow_kgh * s.co2 for s in active),
        "nh3": sum(s.mass_flow_kgh * s.nh3 for s in active),
        "non_condensable": sum(s.mass_flow_kgh * s.non_condensable for s in active),
        "component_15": sum(s.mass_flow_kgh * s.component_15 for s in active),
    }

    # Weight-averaged color and solubility coefficients
    color = sum(s.mass_flow_kgh * s.color_icu for s in active) / total_mass
    a = sum(s.mass_flow_kgh * s.sol_coef_a for s in active) / total_mass
    b = sum(s.mass_flow_kgh * s.sol_coef_b for s in active) / total_mass
    c = sum(s.mass_flow_kgh * s.sol_coef_c for s in active) / total_mass

    # Pressure determination
    if pressure_mode == "minimum":
        press = min(s.pressure_kpa for s in active)
    elif pressure_mode == "maximum":
        press = max(s.pressure_kpa for s in active)
    else:
        press = sum(s.mass_flow_kgh * s.pressure_kpa for s in active) / total_mass

    # Enthalpy conservation: H_total = sum(m_i * h_i)
    total_enthalpy = sum(s.total_enthalpy_flow_kjh for s in active)
    target_h_spec = total_enthalpy / total_mass

    # Normalized fractions
    fractions = {k: v / total_mass for k, v in comp_mass.items()}

    # Temperature solver: find T such that flow_enthalpy(T) == target_h_spec
    # Initial estimate: mass-weighted temperature
    t_est = sum(s.mass_flow_kgh * s.temperature_c for s in active) / total_mass

    # If stream is pure liquid or syrup, invert temperature via Cp
    # Robust Newton-Raphson / bisection
    t_solved = _solve_temp_from_enthalpy(fractions, target_h_spec, press, t_est)

    res = Stream(
        mass_flow_kgh=total_mass,
        temperature_c=t_solved,
        pressure_kpa=press,
        water=fractions["water"],
        dissolved_sucrose=fractions["dissolved_sucrose"],
        non_sucrose_1=fractions["non_sucrose_1"],
        non_sucrose_2=fractions["non_sucrose_2"],
        component_5=fractions["component_5"],
        sucrose_crystals=fractions["sucrose_crystals"],
        fiber_isns=fractions["fiber_isns"],
        cao=fractions["cao"],
        caco3=fractions["caco3"],
        component_10=fractions["component_10"],
        water_vapor=fractions["water_vapor"],
        co2=fractions["co2"],
        nh3=fractions["nh3"],
        non_condensable=fractions["non_condensable"],
        component_15=fractions["component_15"],
        color_icu=color,
        sol_coef_a=a,
        sol_coef_b=b,
        sol_coef_c=c,
    )
    return res.normalize()


def _solve_temp_from_enthalpy(
    fractions: Mapping[str, float],
    target_h: float,
    pressure_kpa: float,
    t_guess: float,
) -> float:
    """Solves temperature in °C matching target specific enthalpy in kJ/kg."""
    t = max(0.0, min(180.0, t_guess))

    # Fast Newton iteration
    for _ in range(20):
        h = flow_enthalpy_kJkg(fractions, t, pressure_kpa)
        diff = h - target_h
        if abs(diff) < 1e-4:
            return t
        # Numerical derivative
        dt = 0.05
        h_plus = flow_enthalpy_kJkg(fractions, t + dt, pressure_kpa)
        cp_eff = max(0.5, (h_plus - h) / dt)
        step = diff / cp_eff
        step = max(-15.0, min(15.0, step))
        t -= step
        t = max(-10.0, min(250.0, t))

    return t
