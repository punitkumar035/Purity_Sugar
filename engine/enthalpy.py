"""
engine/enthalpy.py
Purity for Sugar — Total Stream Enthalpy Module

Authority:
  - Sugar's Help Book Theory.md (Heat Content & Conservation of Energy)
  - CoolProp IAPWS-95 (Water / Steam)
  - Sugar Technologists Manual (Syrup & Crystal Cp)
  - Boynton & Vukov (Minerals & Fiber)
  - Chemical Engineering 1976 (CO2 & NH3)

Rulebook: RULES_v5.md §B7
Calculation Register: CALC-ENT-01

All enthalpies are strictly in kJ/kg with 0°C liquid water reference state.
"""

from __future__ import annotations
import math
from typing import Mapping

from engine.fluids import water_enthalpy_kJkg
from engine.heat_content import (
    cp_syrup,
    cp_sucrose_crystal,
    cp_fiber,
    cp_cao,
    cp_caco3,
    cp_co2_gas,
    cp_nh3_gas,
)

#: Standard 15 component keys from RULES_v5.md §A6
CORE_COMPONENTS = (
    "water",
    "sucrose",
    "invert",
    "ash",
    "ns1",
    "ns2",
    "crystals",
    "fiber",
    "caco3",
    "cao",
    "steamVapour",
    "ethanolL",
    "ethanolG",
    "co2",
    "ammonia",
)

#: Sucrose enthalpy of crystallization in kJ/kg (+54.9 kJ/kg released upon crystallization)
DELTA_H_CRYSTALLIZATION_KJKG = 54.9


def heat_of_crystallization_kJkg() -> float:
    """
    Specific heat of crystallization of sucrose in kJ/kg.
    Positive value indicates heat released (exothermic) when sucrose crystallizes.
    """
    return DELTA_H_CRYSTALLIZATION_KJKG


def heat_of_dissolution_kJkg() -> float:
    """
    Specific heat of dissolution of sucrose in kJ/kg.
    Negative value indicates heat absorbed (endothermic) when crystals dissolve.
    """
    return -DELTA_H_CRYSTALLIZATION_KJKG


def flow_enthalpy_kJkg(
    fractions: Mapping[str, float],
    temp_c: float,
    pressure_kpa: float = 101.325,
) -> float:
    """
    Total specific enthalpy of a multi-component stream in kJ/kg.

    Args:
        fractions: Dictionary mapping component names to mass fractions (0 to 1).
                   Can be normalized or unnormalized (will be normalized internally if sum > 0).
        temp_c: Temperature in °C.
        pressure_kpa: Absolute pressure in kPa.

    Returns:
        Specific enthalpy of the stream in kJ/kg.
    """
    t = temp_c
    p = pressure_kpa

    # Extract component masses/fractions
    def get_val(key: str) -> float:
        return max(0.0, float(fractions.get(key, 0.0) or 0.0))

    w_water = get_val("water")
    w_steam = get_val("steamVapour")
    w_sucrose = get_val("sucrose")
    w_invert = get_val("invert")
    w_ash = get_val("ash")
    w_ns1 = get_val("ns1")
    w_ns2 = get_val("ns2")
    w_crystals = get_val("crystals")
    w_fiber = get_val("fiber")
    w_caco3 = get_val("caco3")
    w_cao = get_val("cao")
    w_ethanol_l = get_val("ethanolL")
    w_ethanol_g = get_val("ethanolG")
    w_co2 = get_val("co2")
    w_nh3 = get_val("ammonia")

    total_mass = (
        w_water
        + w_steam
        + w_sucrose
        + w_invert
        + w_ash
        + w_ns1
        + w_ns2
        + w_crystals
        + w_fiber
        + w_caco3
        + w_cao
        + w_ethanol_l
        + w_ethanol_g
        + w_co2
        + w_nh3
    )

    if total_mass <= 0.0:
        return 0.0

    # Normalize to fraction of 1.0
    scale = 1.0 / total_mass
    w_water *= scale
    w_steam *= scale
    w_sucrose *= scale
    w_invert *= scale
    w_ash *= scale
    w_ns1 *= scale
    w_ns2 *= scale
    w_crystals *= scale
    w_fiber *= scale
    w_caco3 *= scale
    w_cao *= scale
    w_ethanol_l *= scale
    w_ethanol_g *= scale
    w_co2 *= scale
    w_nh3 *= scale

    h_total = 0.0

    # 1. Steam / Water Vapour (via CoolProp, quality=1.0 or superheated)
    if w_steam > 0.0:
        h_steam = water_enthalpy_kJkg(t, p, quality=1.0)
        h_total += w_steam * h_steam

    # 2. Liquid Syrup phase (water + dissolved sugars in unison)
    w_dissolved = w_sucrose + w_invert + w_ash + w_ns1 + w_ns2
    w_liquid_syrup = w_water + w_dissolved

    if w_liquid_syrup > 0.0:
        if w_dissolved > 0.0 and w_water > 0.0:
            # Combined syrup with dissolved solids
            ds = w_dissolved / w_liquid_syrup
            cp = cp_syrup(ds, t)
            h_syrup = cp * t
            h_total += w_liquid_syrup * h_syrup
        elif w_water > 0.0:
            # Pure liquid water (via CoolProp, quality=0.0)
            h_water = water_enthalpy_kJkg(t, p, quality=0.0)
            h_total += w_water * h_water
        else:
            # Dry solids without water
            cp = cp_syrup(1.0, t)
            h_total += w_dissolved * cp * t

    # 3. Sucrose Crystals (solid phase)
    if w_crystals > 0.0:
        cp_cryst = cp_sucrose_crystal(t)
        h_total += w_crystals * (cp_cryst * t)

    # 4. Insoluble Fiber / Marc
    if w_fiber > 0.0:
        cp_fib = cp_fiber(t, moisture_frac=0.0)
        h_total += w_fiber * (cp_fib * t)

    # 5. Limestone (CaCO3) and Lime (CaO)
    if w_caco3 > 0.0:
        h_total += w_caco3 * (cp_caco3(t) * t)
    if w_cao > 0.0:
        h_total += w_cao * (cp_cao(t) * t)

    # 6. Gases (CO2, NH3)
    if w_co2 > 0.0:
        h_total += w_co2 * (cp_co2_gas(t) * t)
    if w_nh3 > 0.0:
        h_total += w_nh3 * (cp_nh3_gas(t) * t)

    # 7. Ethanol (liquid Cp ≈ 2.44 kJ/kg·K; latent heat ≈ 846 kJ/kg)
    if w_ethanol_l > 0.0:
        h_total += w_ethanol_l * (2.44 * t)
    if w_ethanol_g > 0.0:
        h_total += w_ethanol_g * (2.44 * t + 846.0)

    return h_total
