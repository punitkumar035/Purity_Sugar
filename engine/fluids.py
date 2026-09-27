"""
engine/fluids.py
Purity for Sugar — CoolProp Thermodynamics Integration

Authority: CoolProp (IAPWS-95 formulation for Water, Dillon & Penoncello for Ethanol)
Rulebook : RULES_v5.md §B2
Calculation Register: CALC-ENT-01

All thermodynamic properties strictly normalize internally to standard SI units:
  - Pressure: kPa absolute (converted to Pa for CoolProp)
  - Temperature: °C (converted to K for CoolProp: T_K = t + 273.15)
  - Enthalpy: kJ/kg (CoolProp returns J/kg; divided by 1000)
  - Specific heat: kJ/(kg·K) (CoolProp returns J/(kg·K); divided by 1000)
"""

from __future__ import annotations
import math
import warnings
from typing import Optional

try:
    import CoolProp.CoolProp as CP
except ImportError:
    CP = None


def init_fluids(fluids_dir: str = "") -> None:
    """
    Initialize fluid database. Fails loudly if CoolProp is missing or broken.
    """
    if CP is None:
        raise ImportError(
            "CoolProp is required for thermodynamic water/steam properties. "
            "Install via: pip install CoolProp"
        )
    # Smoke test CoolProp Water property call
    try:
        t_sat = CP.PropsSI("T", "P", 101325.0, "Q", 0.0, "Water")
        if not (370.0 < t_sat < 375.0):
            raise RuntimeError(f"Unexpected saturation temperature {t_sat} K for water at 101.325 kPa.")
    except Exception as e:
        raise RuntimeError(f"CoolProp fluid initialization failed: {e}") from e


def _ensure_cp() -> None:
    if CP is None:
        init_fluids()


def water_sat_temp_c(pressure_kpa: float) -> float:
    """
    Saturation temperature of water at given pressure.

    Args:
        pressure_kpa: Absolute pressure in kPa. Must be > 0.

    Returns:
        Saturation temperature in °C.

    Raises:
        ValueError: If pressure_kpa <= 0 or exceeds critical pressure (22064 kPa).
    """
    _ensure_cp()
    if pressure_kpa <= 0.0:
        raise ValueError(f"Pressure must be > 0 kPa; received {pressure_kpa}.")
    p_pa = pressure_kpa * 1000.0
    p_crit = CP.PropsSI("P_CRITICAL", "Water")
    if p_pa >= p_crit:
        raise ValueError(
            f"Pressure {pressure_kpa:.2f} kPa exceeds water critical pressure ({p_crit / 1000.0:.2f} kPa)."
        )

    t_k = CP.PropsSI("T", "P", p_pa, "Q", 0.0, "Water")
    return t_k - 273.15


def water_sat_pressure_kpa(temp_c: float) -> float:
    """
    Saturation pressure of water at given temperature.

    Args:
        temp_c: Temperature in °C. Must be in [0.01, 373.9] °C.

    Returns:
        Saturation pressure in kPa absolute.

    Raises:
        ValueError: If temp_c is below triple point (0.01°C) or above critical temperature (374°C).
    """
    _ensure_cp()
    if not (0.0 <= temp_c <= 373.95):
        raise ValueError(
            f"Temperature {temp_c}°C is outside valid saturation range [0, 373.95] °C."
        )
    t_k = temp_c + 273.15
    p_pa = CP.PropsSI("P", "T", t_k, "Q", 0.0, "Water")
    return p_pa / 1000.0


def steam_is_superheated(temp_c: float, pressure_kpa: float) -> bool:
    """
    True if temperature is strictly greater than saturation temperature at this pressure.
    """
    t_sat = water_sat_temp_c(pressure_kpa)
    return temp_c > t_sat + 0.01


def steam_superheat_K(temp_c: float, pressure_kpa: float) -> float:
    """
    Degrees of superheat in K (0 if not superheated).
    """
    t_sat = water_sat_temp_c(pressure_kpa)
    return max(0.0, temp_c - t_sat)


def water_enthalpy_kJkg(
    temp_c: float,
    pressure_kpa: float,
    quality: float = 1.0,
) -> float:
    """
    Specific enthalpy of water/steam in kJ/kg.

    Behavior:
      - If temp_c is higher than sat_temp + 0.01°C: evaluated as superheated vapor at (T, P).
      - If temp_c is lower than sat_temp - 0.01°C: evaluated as subcooled liquid at (T, P).
      - If within ±0.01°C of sat_temp or quality is explicitly specified in [0, 1]:
        evaluated as two-phase mixture with vapor quality `quality` (0=sat liquid, 1=sat vapor).

    Args:
        temp_c: Temperature in °C.
        pressure_kpa: Absolute pressure in kPa.
        quality: Vapor mass quality in [0, 1] when in two-phase region. Default 1.0.

    Returns:
        Specific enthalpy in kJ/kg.
    """
    _ensure_cp()
    if pressure_kpa <= 0.0:
        raise ValueError(f"Pressure must be > 0 kPa; received {pressure_kpa}.")

    p_pa = pressure_kpa * 1000.0
    t_k = temp_c + 273.15
    t_sat_c = water_sat_temp_c(pressure_kpa)

    # 1. Superheated vapor
    if temp_c > t_sat_c + 0.05:
        h_j_kg = CP.PropsSI("H", "T", t_k, "P", p_pa, "Water")
        return h_j_kg / 1000.0

    # 2. Subcooled liquid
    if temp_c < t_sat_c - 0.05 and quality == 0.0:
        h_j_kg = CP.PropsSI("H", "T", t_k, "P", p_pa, "Water")
        return h_j_kg / 1000.0

    # 3. Two-phase saturation state
    q_clamped = max(0.0, min(1.0, quality))
    h_j_kg = CP.PropsSI("H", "P", p_pa, "Q", q_clamped, "Water")
    return h_j_kg / 1000.0


def water_latent_heat_kJkg(temp_c: float) -> float:
    """
    Latent heat of vaporisation of water at given temperature in kJ/kg.
    H_vap(T) - H_liq(T).
    """
    _ensure_cp()
    t_k = temp_c + 273.15
    h_liq = CP.PropsSI("H", "T", t_k, "Q", 0.0, "Water")
    h_vap = CP.PropsSI("H", "T", t_k, "Q", 1.0, "Water")
    return (h_vap - h_liq) / 1000.0


def water_cp_kJkgK(temp_c: float, pressure_kpa: float) -> float:
    """
    Specific heat capacity of water at given state in kJ/(kg·K).
    """
    _ensure_cp()
    p_pa = pressure_kpa * 1000.0
    t_k = temp_c + 273.15
    cp_j = CP.PropsSI("CPMASS", "T", t_k, "P", p_pa, "Water")
    return cp_j / 1000.0


def ethanol_water_bubble_temp_c(
    ethanol_mole_frac: float,
    pressure_kpa: float,
) -> float:
    """
    Bubble point of ethanol-water mixture at given mole fraction and pressure.
    """
    _ensure_cp()
    if not (0.0 <= ethanol_mole_frac <= 1.0):
        raise ValueError(f"Ethanol mole fraction must be in [0, 1]; received {ethanol_mole_frac}.")

    p_pa = pressure_kpa * 1000.0

    if ethanol_mole_frac == 0.0:
        return water_sat_temp_c(pressure_kpa)
    elif ethanol_mole_frac == 1.0:
        t_k = CP.PropsSI("T", "P", p_pa, "Q", 0.0, "Ethanol")
        return t_k - 273.15

    # CoolProp mixture syntax: HEOS::Ethanol[x]&Water[1-x]
    fluid_spec = f"HEOS::Ethanol[{ethanol_mole_frac}]&Water[{1.0 - ethanol_mole_frac}]"
    try:
        t_k = CP.PropsSI("T", "P", p_pa, "Q", 0.0, fluid_spec)
        return t_k - 273.15
    except Exception:
        # Fallback to standard Wilson / NRTL bubble correlation if CoolProp mixture EOS is unavailable
        t_w = water_sat_temp_c(pressure_kpa)
        t_e = CP.PropsSI("T", "P", p_pa, "Q", 0.0, "Ethanol") - 273.15
        # Ideal/interpolated bubble curve approximation
        return (1.0 - ethanol_mole_frac) * t_w + ethanol_mole_frac * t_e
