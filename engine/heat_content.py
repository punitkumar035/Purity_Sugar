"""
engine/heat_content.py
Purity for Sugar — Specific Heat Capacity Module

Authority:
  - Sugar Technologists Manual (Bartens, 8th ed.)
    - Syrup Cp: eq 341/3
    - Sucrose crystal Cp: eq 311/2
  - Robert S. Boynton: Chemistry and Technology of Lime and Limestone (CaCO3, CaO, Ca(OH)2)
  - Konstantin Vukov: Physics and Chemistry of Sugar Beet in Sugar Manufacture (Fiber / Marc)
  - Chemical Engineering (Aug 16, 1976): CO2 and NH3 gases
  - CoolProp (IAPWS-95): Liquid water and water vapor

Rulebook: RULES_v5.md §B5
Calculation Register: CALC-CP-01, CALC-CP-02
Units policy: Specific heat capacity is strictly in kJ/(kg·K).
              Temperature is in °C; pressure in kPa absolute; DS in fraction (0–1).
"""

from __future__ import annotations
import math
from engine.fluids import water_cp_kJkgK


def cp_syrup(ds_frac: float, temp_c: float) -> float:
    """
    Specific heat capacity of sugar syrup in kJ/(kg·K).

    Source: Sugar Technologists Manual 8th ed, eq 341/3:
            Cp_syrup = (4.187 − 2.884·DS) + (0.00604 − 0.00382·DS)·t

    Args:
        ds_frac: Dry substance fraction in [0, 1].
        temp_c:  Temperature in °C.

    Returns:
        Cp in kJ/(kg·K).

    Raises:
        ValueError: If ds_frac is outside [0, 1].
    """
    if not (0.0 <= ds_frac <= 1.0):
        raise ValueError(f"Dry substance fraction must be in [0, 1]; received {ds_frac}.")

    ds = ds_frac
    t = temp_c
    cp = (4.187 - 2.884 * ds) + (0.00604 - 0.00382 * ds) * t
    return cp


def cp_sucrose_crystal(temp_c: float) -> float:
    """
    Specific heat capacity of sucrose crystals in kJ/(kg·K).

    Source: Sugar Technologists Manual 8th ed, eq 311/2:
            Cp_crystal = 1.2473 + 0.002096·t − 3.9e-6·t²

    Args:
        temp_c: Temperature in °C. Valid range: −20 to 140 °C.

    Returns:
        Cp in kJ/(kg·K).
    """
    t = temp_c
    cp = 1.2473 + 0.002096 * t - 3.9e-6 * (t**2)
    return cp


def cp_water_liquid(temp_c: float, pressure_kpa: float = 101.325) -> float:
    """
    Specific heat capacity of liquid water in kJ/(kg·K) via CoolProp.
    """
    return water_cp_kJkgK(temp_c, pressure_kpa)


def cp_water_vapor(temp_c: float, pressure_kpa: float = 101.325) -> float:
    """
    Specific heat capacity of water vapor in kJ/(kg·K) via CoolProp.
    """
    return water_cp_kJkgK(temp_c, pressure_kpa)


def cp_caco3(temp_c: float) -> float:
    """
    Specific heat capacity of limestone (CaCO3) in kJ/(kg·K).

    Source: Boynton, Chemistry and Technology of Lime and Limestone:
            Cp = 0.819 + 0.000234·t − 20700 / T²   [T in K]
    """
    t = temp_c
    t_k = t + 273.15
    return 0.819 + 0.000234 * t - 20700.0 / (t_k**2)


def cp_cao(temp_c: float) -> float:
    """
    Specific heat capacity of quicklime (CaO) in kJ/(kg·K).

    Source: Boynton, Chemistry and Technology of Lime and Limestone:
            Cp = 0.753 + 0.000117·t − 11700 / T²   [T in K]
    """
    t = temp_c
    t_k = t + 273.15
    return 0.753 + 0.000117 * t - 11700.0 / (t_k**2)


def cp_ca_oh2(temp_c: float) -> float:
    """
    Specific heat capacity of hydrated lime (Ca(OH)2) in kJ/(kg·K).
    Approximately 1.30 kJ/(kg·K) over 0–200 °C.
    """
    return 1.30


def cp_fiber(temp_c: float, moisture_frac: float = 0.0) -> float:
    """
    Specific heat capacity of cane fiber / beet marc in kJ/(kg·K).

    Source: Konstantin Vukov, Physics and Chemistry of Sugar Beet in Sugar Manufacture:
            Cp_marc = 1.25 + 0.0034 · moisture_pct
    """
    m_pct = max(0.0, min(100.0, moisture_frac * 100.0))
    return 1.25 + 0.0034 * m_pct


def cp_co2_gas(temp_c: float) -> float:
    """
    Specific heat capacity of CO2 gas in kJ/(kg·K).

    Source: Chemical Engineering, Aug 16, 1976:
            Cp = A + B·T + C·T² + D·T³  [J/(mol·K), T in K]
            A = 19.795, B = 0.07344, C = -5.602e-5, D = 1.715e-8
            MW = 44.01 g/mol
    """
    t_k = temp_c + 273.15
    cp_j_mol = (
        19.795
        + 0.07344 * t_k
        - 5.602e-5 * (t_k**2)
        + 1.715e-8 * (t_k**3)
    )
    # J/(mol·K) / (g/mol) = J/(g·K) = kJ/(kg·K)
    return cp_j_mol / 44.01


def cp_nh3_gas(temp_c: float) -> float:
    """
    Specific heat capacity of NH3 gas in kJ/(kg·K).

    Source: Chemical Engineering, Aug 16, 1976:
            Cp = A + B·T + C·T²  [J/(mol·K), T in K]
            A = 27.568, B = 0.02563, C = 9.890e-6
            MW = 17.03 g/mol
    """
    t_k = temp_c + 273.15
    cp_j_mol = (
        27.568
        + 0.02563 * t_k
        + 9.890e-6 * (t_k**2)
    )
    return cp_j_mol / 17.03
