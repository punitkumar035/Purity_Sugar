"""
engine/density.py
Purity for Sugar — Density (Specific Weight) Module

Authority:
  - Rein, Cane Sugar Engineering (Eq. 32.8 citing Lyle 1957)
  - Sugar's Help Book Theory.md & Centrifugal evaluation (Centrifugal_Scn-1.png)
  - Bubník-Kadlec (1995): Sugar Technologists Manual

Rulebook: RULES_v5.md §B8
Calculation Register: CALC-DEN-01
Units policy: Density is strictly in kg/m³.
              Dry substance in fraction (0–1); Temperature in °C.
"""

from __future__ import annotations
import math

#: Literature sucrose crystal density at 20°C (kg/m³)
RHO_SUCROSE_CRYSTAL_20C = 1587.0


def crystal_density_kgm3(temp_c: float = 20.0) -> float:
    """
    Density of pure sucrose crystals in kg/m³.
    Literature reference: 1587.0 kg/m³ (Sugar Technologists Manual).
    """
    return RHO_SUCROSE_CRYSTAL_20C


def syrup_density_kgm3(ds_frac: float, temp_c: float) -> float:
    """
    Density of sugar syrup / technical liquor in kg/m³.

    Source: Rein, Cane Sugar Engineering Eq. 32.8 citing Lyle (1957):
            rho = 1000 · [1 + W·(W + 200)/54000] · [1 − 0.036·(T − 20)/(160 − T)]
            where W = ds_frac · 100, T = temp_c.

    Args:
        ds_frac: Dry substance fraction in [0, 1).
        temp_c:  Temperature in °C. Valid range: 0–140 °C.

    Returns:
        Density in kg/m³.

    Raises:
        ValueError: If ds_frac or temp_c outside physical bounds.
    """
    if not (0.0 <= ds_frac < 1.0):
        raise ValueError(f"Dry substance fraction must be in [0, 1); received {ds_frac}.")
    if not (-10.0 <= temp_c <= 150.0):
        raise ValueError(f"Temperature {temp_c}°C is outside valid range (-10 to 150°C).")
    if abs(160.0 - temp_c) < 1.0:
        raise ValueError(f"Temperature {temp_c}°C is too close to singularity of Lyle correlation (160°C).")

    w = ds_frac * 100.0
    t = temp_c

    rho = 1000.0 * (1.0 + w * (w + 200.0) / 54000.0) * (1.0 - 0.036 * (t - 20.0) / (160.0 - t))
    return max(500.0, rho)


def massecuite_density_kgm3(
    ds_mc: float,
    pu_mc: float,
    crystal_frac: float,
    temp_c: float,
) -> float:
    """
    Density of massecuite in kg/m³.

    Calculated via two-phase harmonic volume addition:
      1/rho_mc = Cry / rho_crystal + (1 - Cry) / rho_ml
    where rho_ml is the mother liquor density evaluated at DS_ml and T.

    Authority:
      Sugar's Help Book Theory.md & Centrifugal evaluation (Centrifugal_Scn-1.png:
      DSmc=93%, PUmc=86.44%, T=81°C, Cry=47.44% -> Density = 1493.84 kg/m³).

    Args:
        ds_mc:        Overall massecuite dry substance fraction in (0, 1).
        pu_mc:        Overall massecuite purity fraction in (0, 1].
        crystal_frac: Crystal weight fraction in massecuite in [0, ds_mc).
        temp_c:       Temperature in °C.

    Returns:
        Massecuite density in kg/m³.

    Raises:
        ValueError: If crystal_frac is invalid or mother liquor fraction <= 0.
    """
    if not (0.0 < ds_mc < 1.0):
        raise ValueError(f"Massecuite DS must be in (0, 1); received {ds_mc}.")
    if not (0.0 <= crystal_frac < ds_mc):
        raise ValueError(f"Crystal fraction {crystal_frac} must be in [0, DSmc={ds_mc}).")

    if crystal_frac <= 0.0:
        return syrup_density_kgm3(ds_mc, temp_c)

    w_ml = 1.0 - crystal_frac
    ds_ml = (ds_mc - crystal_frac) / w_ml

    rho_ml = syrup_density_kgm3(ds_ml, temp_c)
    rho_cryst = crystal_density_kgm3(temp_c)

    # Specific volume harmonic weighting
    vol_specific = (crystal_frac / rho_cryst) + (w_ml / rho_ml)
    if vol_specific <= 0.0:
        raise ValueError("Specific volume of massecuite non-positive.")

    return 1.0 / vol_specific
