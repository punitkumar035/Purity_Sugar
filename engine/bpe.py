"""
engine/bpe.py
Purity for Sugar — Boiling Point Elevation (BPE) Module

Authority:
  - Kadlec, Bretschneider and Dandor (KBD 1978): "Boiling Point Elevation of Sugar Solutions",
    La Sucrerie Belge, Vol. 97.
  - Bubník & Kadlec (1995): Sugar Technologists Manual (Bartens).
  - Sugar's Help Book Theory.md (Boiling Point Elevation section).

Rulebook: RULES_v5.md §B6
Calculation Register: CALC-BPE-01

Units policy:
  - Pressure: kPa absolute
  - Temperature: °C
  - Dry substance and purity: fractions (0–1)
  - BPE: °C (dimensionless temperature difference ΔT)
"""

from __future__ import annotations
import math
from typing import Optional

from engine.fluids import water_sat_temp_c, water_sat_pressure_kpa


def bpe_kbd_1978_pure(pressure_kpa: float, sucrose_mass_frac: float) -> float:
    """
    KBD (1978) boiling point elevation for pure sucrose in water.

    Source: Kadlec, Bretschneider and Dandor (1978), La Sucrerie Belge 97:
            xB = mole fraction of sucrose
            poly = 33.003·xB + 170.517·xB² − 324.177·xB³ + 172.554·xB⁴
            BPE = (r(373.15) / r(T0)) · (T0 / 373.15)² · poly

    Args:
        pressure_kpa: Absolute pressure in kPa.
        sucrose_mass_frac: Sucrose mass fraction in [0, 1).

    Returns:
        BPE in °C (>= 0).
    """
    if not (0.0 <= sucrose_mass_frac < 1.0):
        raise ValueError(
            f"Sucrose mass fraction must be in [0, 1); received {sucrose_mass_frac}."
        )
    if sucrose_mass_frac <= 0.0:
        return 0.0

    t0 = water_sat_temp_c(pressure_kpa)
    ws = sucrose_mass_frac
    m_s = 342.2965
    m_w = 18.01528
    x_b = (ws / m_s) / ((ws / m_s) + ((1.0 - ws) / m_w))

    t0_k = t0 + 273.15

    def r_heat(t_k: float) -> float:
        return (
            60347.4
            - 169.558 * t_k
            + 0.858193 * (t_k**2)
            - 2.11784e-3 * (t_k**3)
            + 1.76e-6 * (t_k**4)
        )

    poly = (
        33.003 * x_b
        + 170.517 * (x_b**2)
        - 324.177 * (x_b**3)
        + 172.554 * (x_b**4)
    )

    r_ratio = r_heat(373.15) / r_heat(t0_k)
    bpe = r_ratio * ((t0_k / 373.15) ** 2) * poly
    return max(0.0, bpe)


def bpe_bubnik_kadlec(
    ds_frac: float,
    purity_frac: float,
    t_sat_water_c: float,
) -> float:
    """
    Bubník-Kadlec (1995) technical boiling point elevation for factory sugar solutions.

    Accounts for dry substance (WDS), purity (Q), and water boiling temperature (t).

    Args:
        ds_frac: Dry substance fraction in [0, 0.98].
        purity_frac: Solution purity fraction in [0, 1.0].
        t_sat_water_c: Pure water boiling temperature at ambient pressure in °C.

    Returns:
        BPE in °C (>= 0).
    """
    if ds_frac <= 0.0:
        return 0.0
    if not (0.0 <= ds_frac <= 0.98):
        raise ValueError(f"Dry substance fraction {ds_frac} is outside physical range [0, 0.98].")
    if not (0.0 <= purity_frac <= 1.0):
        raise ValueError(f"Purity fraction {purity_frac} must be in [0, 1].")

    w = ds_frac * 100.0
    q = purity_frac * 100.0
    t = t_sat_water_c

    if t >= 374.3:
        raise ValueError(f"Water boiling temperature {t}°C exceeds critical point.")

    if w < 60.0:
        k = 40.0
        a0, a1, a2 = 1.59515e-4, -2.00092e-6, 8.01933e-9
        b0, b1, b2 = 1.84440e-6, -3.04380e-8, 1.72958e-10
        c0, c1, c2 = 1.08062e-3, 2.89645e-6, -3.01416e-8
    else:
        k = 60.0
        a0, a1, a2 = 1.67525e-4, -1.85299e-6, 7.92284e-9
        b0, b1, b2 = 2.87764e-6, -2.77263e-8, 1.44306e-10
        c0, c1, c2 = 1.06668e-3, 2.10304e-6, -4.28274e-8

    a_b = a0 + a1 * q + a2 * q * q
    b_b = b0 + b1 * q + b2 * q * q
    c_b = c0 + c1 * q + c2 * q * q

    denominator = (374.3 - t) ** 0.38
    if denominator <= 0.0:
        return 0.0

    bpe = a_b * (w**2) * (((273.15 + t) ** 2) / denominator) * (b_b * ((w - k) ** 2) + c_b)
    return max(0.0, bpe)


def bpe_celsius(
    ds_frac: float,
    purity_frac: float,
    pressure_kpa: float,
) -> float:
    """
    Standard Sugar Engineering Boiling Point Elevation.

    Source: Sugar's Help Book Theory.md (Boiling Point Elevation section)
            CALC-BPE-01: Pure water (DS=0) has BPE = 0.0 °C.

    Args:
        ds_frac: Dry substance fraction (0 to 1).
        purity_frac: Purity fraction (0 to 1).
        pressure_kpa: Absolute operating pressure in kPa.

    Returns:
        BPE in °C (>= 0).
    """
    if ds_frac <= 0.0:
        return 0.0
    t_sat = water_sat_temp_c(pressure_kpa)
    return bpe_bubnik_kadlec(ds_frac, purity_frac, t_sat)


def boiling_temp_c(
    ds_frac: float,
    purity_frac: float,
    pressure_kpa: float,
    bpe_factor: float = 1.0,
) -> float:
    """
    Boiling temperature of the sugar solution:
    T_boil = T_sat(P) + BPE · bpe_factor.
    """
    t_sat = water_sat_temp_c(pressure_kpa)
    bpe = bpe_celsius(ds_frac, purity_frac, pressure_kpa)
    return t_sat + bpe * bpe_factor


def vapor_sat_temp_from_boiling(
    boiling_temp_c_val: float,
    ds_frac: float,
    purity_frac: float,
    bpe_factor: float = 1.0,
    tol: float = 1e-5,
    max_iter: int = 50,
) -> float:
    """
    Inverse: given known boiling temperature and solution properties,
    iteratively solve for vapor saturation temperature:
      T_sat = T_boil − BPE(DS, PU, T_sat) · bpe_factor
    """
    if ds_frac <= 0.0:
        return boiling_temp_c_val

    # Initial guess: assume BPE ≈ 2°C
    t_sat = boiling_temp_c_val - 2.0
    for _ in range(max_iter):
        bpe = bpe_bubnik_kadlec(ds_frac, purity_frac, t_sat)
        t_sat_next = boiling_temp_c_val - bpe * bpe_factor
        if abs(t_sat_next - t_sat) < tol:
            return t_sat_next
        # Damped update
        t_sat = 0.5 * (t_sat + t_sat_next)

    return t_sat


def pressure_from_vapor_temp(vapor_sat_temp_c: float) -> float:
    """
    Vapor saturation pressure from saturation temperature in kPa.
    """
    return water_sat_pressure_kpa(vapor_sat_temp_c)
