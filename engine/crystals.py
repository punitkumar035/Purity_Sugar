"""
engine/crystals.py
Purity for Sugar — Crystal Content Module (Forward and Inverse)

Authority: Sugar's Help Book → Theory.md (Crystal Content section)
           Screenshot reference: Centrifugal_Scn-1.png
Rulebook : RULES_v5.md §B4
Calculation Register: CALC-CRY-01, CALC-CRY-02

Equations implemented:
  1. Forward calculation:
     Given massecuite DS (DSmc), purity (PUmc), temperature (T), supersaturation (Ss),
     and solubility coefficients (a, b, c):
       - NSW = (1 - PUmc) · DSmc / (1 - DSmc)
       - Sc = saturation_coefficient(NSW, a, b, c)
       - S = sucrose_saturation_pct(T)
       - Rsat = Sc · (S / (100 - S))
       - Rml = Ss · Rsat  (sucrose to water in mother liquor)
       - ml_dry = Rml + NSW
       - DSml = ml_dry / (1 + ml_dry)
       - PUml = Rml / ml_dry
       - Cry = (DSmc - DSml) / (1 - DSml)

  2. Inverse calculation:
     Given massecuite DS (DSmc), purity (PUmc), and crystal fraction (Cry):
       - DSml = (DSmc - Cry) / (1 - Cry)
       - PUml = (PUmc · DSmc - Cry) / (DSmc - Cry)

Units policy: All DS, purity, and crystal content values are FRACTIONS (0–1).
              Temperature is in °C.
"""

from __future__ import annotations
import math
from typing import TypedDict

from engine.solubility import (
    sucrose_saturation_pct,
    saturation_coefficient,
    supersaturation,
)


class CrystalsForwardResult(TypedDict):
    crystal_frac: float
    ds_ml: float
    pu_ml: float
    nsw: float
    ss_calc: float


class CrystalsInverseResult(TypedDict):
    ds_ml: float
    pu_ml: float


def crystals_forward(
    ds_mc: float,
    pu_mc: float,
    temp_c: float,
    ss: float,
    a: float,
    b: float,
    c: float,
) -> CrystalsForwardResult:
    """
    Forward crystal content calculation.
    Calculates crystal fraction and mother liquor state from massecuite parameters.

    Governing Authority:
        Sugar's Help Book Theory.md (Crystal Content section & Centrifugal_Scn-1.png).

    Args:
        ds_mc:  Massecuite dry substance fraction in (0, 1).
        pu_mc:  Massecuite true purity fraction in (0, 1].
        temp_c: Massecuite temperature in °C.
        ss:     Target mother liquor supersaturation (dimensionless, > 0).
        a, b, c: Melassigenic solubility coefficients.

    Returns:
        CrystalsForwardResult dictionary:
            crystal_frac: Crystal weight fraction in massecuite (0 to ds_mc).
            ds_ml:        Mother liquor dry substance fraction.
            pu_ml:        Mother liquor purity fraction.
            nsw:          Non-sucrose to water ratio (dimensionless).
            ss_calc:      Calculated supersaturation of resulting mother liquor.

    Raises:
        ValueError: If inputs exceed physical validity boundaries.
    """
    if not (0.0 < ds_mc < 1.0):
        raise ValueError(f"Massecuite DS must be in (0, 1); received {ds_mc}.")
    if not (0.0 < pu_mc <= 1.0):
        raise ValueError(f"Massecuite purity must be in (0, 1]; received {pu_mc}.")
    if not (ss > 0.0):
        raise ValueError(f"Supersaturation must be > 0; received {ss}.")

    water_mc = 1.0 - ds_mc
    ns_mc = ds_mc * (1.0 - pu_mc)
    nsw = ns_mc / water_mc

    # Impurity saturation coefficient & pure sucrose saturation
    sc = saturation_coefficient(nsw, a, b, c)
    s_pct = sucrose_saturation_pct(temp_c)

    denom_pure = 100.0 - s_pct
    if denom_pure <= 0.0:
        raise ValueError(f"Pure saturation S={s_pct:.4f} >= 100 at T={temp_c}°C.")

    # Saturated sucrose-to-water ratio
    r_sat = sc * (s_pct / denom_pure)

    # Mother liquor sucrose-to-water ratio at specified supersaturation
    r_ml = ss * r_sat

    # Mother liquor dry solids per unit water = dissolved sucrose + non-sucrose
    ml_dry = r_ml + nsw
    ds_ml = ml_dry / (1.0 + ml_dry)
    pu_ml = r_ml / ml_dry if ml_dry > 0 else 0.0

    # Crystals fraction from solids conservation (DScs = PUcs = 1.0)
    denom_cry = 1.0 - ds_ml
    if denom_cry <= 0.0:
        raise ValueError(f"Mother liquor DS={ds_ml:.6f} >= 1.0: non-physical solution.")

    cry = (ds_mc - ds_ml) / denom_cry

    # Cross-check calculated supersaturation
    ss_calc = supersaturation(ds_ml, pu_ml, temp_c, a, b, c)

    return {
        "crystal_frac": cry,
        "ds_ml": ds_ml,
        "pu_ml": pu_ml,
        "nsw": nsw,
        "ss_calc": ss_calc,
    }


def crystals_inverse(
    ds_mc: float,
    pu_mc: float,
    crystal_frac: float,
) -> CrystalsInverseResult:
    """
    Inverse crystal content calculation.
    Calculates mother liquor DS and purity when crystal fraction is known.

    Governing Authority:
        Sugar's Help Book Theory.md (Crystal Content section, eq. CrystalContent-3.gif).
        Assuming pure sucrose crystals: DScs = PUcs = 1.0.

    Args:
        ds_mc:        Massecuite dry substance fraction in (0, 1).
        pu_mc:        Massecuite true purity fraction in (0, 1].
        crystal_frac: Known crystal weight fraction in massecuite [0, ds_mc).

    Returns:
        CrystalsInverseResult dictionary:
            ds_ml: Mother liquor dry substance fraction.
            pu_ml: Mother liquor purity fraction.

    Raises:
        ValueError: If crystal_frac is >= 1.0 or >= ds_mc.
    """
    if not (0.0 < ds_mc < 1.0):
        raise ValueError(f"Massecuite DS must be in (0, 1); received {ds_mc}.")
    if not (0.0 < pu_mc <= 1.0):
        raise ValueError(f"Massecuite purity must be in (0, 1]; received {pu_mc}.")
    if not (0.0 <= crystal_frac < ds_mc):
        raise ValueError(
            f"Crystal fraction {crystal_frac} must be in [0, DSmc={ds_mc})."
        )

    w_ml = 1.0 - crystal_frac
    if w_ml <= 0.0:
        raise ValueError("Mother liquor fraction must be positive.")

    ds_ml = (ds_mc - crystal_frac) / w_ml
    dry_ml = ds_mc - crystal_frac
    if dry_ml <= 0.0:
        raise ValueError("Mother liquor dry substance is zero or negative.")

    pu_ml = (pu_mc * ds_mc - crystal_frac) / dry_ml

    return {
        "ds_ml": ds_ml,
        "pu_ml": pu_ml,
    }


def massecuite_crystal_content(
    ds_mc: float,
    pu_mc: float,
    temp_c: float,
    ss: float,
    a: float,
    b: float,
    c: float,
) -> float:
    """
    Convenience function returning the crystal weight fraction directly.
    """
    res = crystals_forward(ds_mc, pu_mc, temp_c, ss, a, b, c)
    return res["crystal_frac"]
