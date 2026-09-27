"""
engine/solubility.py
Purity for Sugar — Sucrose Solubility & Supersaturation Module

Authority: Sugar's Help Book → Theory/Theory.md (Sucrose Solubility section)
Rulebook : RULES_v5.md §B3

Equations implemented:
  1. Vavrinecz (ICUMSA official) — pure sucrose saturation   [§B3.1]
  2. Vavrinecz saturation coefficient (c ≠ 0)               [§B3.2]
  3. Wagnerowski saturation coefficient (c = 0)              [§B3.3]
  4. NSW — non-sucrose to water ratio                        [§B3.4]
  5. Van Hook supersaturation (ICUMSA official)              [§B3.5]

Units policy: DS and purity are FRACTIONS (0–1); temperature is °C.
"""

from __future__ import annotations
import math
import warnings


# ---------------------------------------------------------------------------
# 1. Vavrinecz — pure sucrose saturation
# ---------------------------------------------------------------------------

def sucrose_saturation_pct(temp_c: float) -> float:
    """
    Vavrinecz equation — ICUMSA official.
    Returns weight-% of sucrose in saturated pure sucrose solution.

    Source: Sugar's Help Book → Theory.md (Sucrose Solubility section, image SucroseSolubiliby-1.gif)
            S(t) = 64.447 + 0.08222·t + 1.6169e-3·t² − 1.558e-6·t³ − 4.63e-8·t⁴

    Args:
        temp_c: Temperature in °C. Valid range: −10 to 100 °C.

    Returns:
        S: weight-% sucrose at saturation (dimensionless, range ≈ 64–83 %).

    Raises:
        ValueError: if temp_c is outside physical bounds (−15 to 125 °C).
    """
    if not (-15.0 <= temp_c <= 125.0):
        raise ValueError(
            f"Temperature {temp_c}°C is outside the valid range for "
            f"Vavrinecz sucrose solubility (−15 to 125°C)."
        )
    t = temp_c
    S = 64.447 + 0.08222 * t + 1.6169e-3 * t**2 - 1.558e-6 * t**3 - 4.63e-8 * t**4
    return S


# ---------------------------------------------------------------------------
# 2 & 3. Saturation coefficient — Vavrinecz (c≠0) or Wagnerowski (c=0)
# ---------------------------------------------------------------------------

#: Reference coefficients from Sugar's Help Book Theory.md
SATURATION_COEFFICIENTS: dict[str, tuple[float, float, float]] = {
    "BEET_GRUT":    (0.178,  0.82, -2.1),   # Beet — Grut values
    "BEET_POLISH":  (0.27,   0.71, -1.4),   # Beet — Polish values
    "CANE_TYPICAL": (0.04,   0.71, -2.1),   # Cane typical
    "WAGNEROWSKI":  (0.036,  1.0,   0.0),   # Wagnerowski (c=0 triggers Sc = a·NSW + b)
}

#: NSW range for Wagnerowski validity (RULES_v5.md §B3.3, Theory.md)
_WAGNEROWSKI_NSW_MIN = 1.6
_WAGNEROWSKI_NSW_MAX = 3.5


def saturation_coefficient(
    nsw: float,
    a: float,
    b: float,
    c: float,
) -> float:
    """
    Saturation coefficient Sc for a solution with impurities.

    Source: Sugar's Help Book → Theory.md
            - Vavrinecz (c ≠ 0):
                Sc = a·NSW + b + (1 − b)·exp(c·NSW)      [SucroseSolubility-2.gif]
            - Wagnerowski (c == 0):
                Sc = a·NSW + b                           [SucroseSolubility-3.gif]

    Wagnerowski is valid ONLY for NSW in [1.6, 3.5].
    If c=0 and NSW < 1.6, the Vavrinecz function should be used instead
    (pass a valid c value). This function will raise a warning if
    Wagnerowski is called with NSW outside [1.6, 3.5].

    Args:
        nsw: Non-sucrose to water ratio (weight basis). Must be ≥ 0.
        a, b, c: Solubility coefficients (from stream or station property).

    Returns:
        Sc: Saturation coefficient (dimensionless, typically 0.50–2.00).

    Raises:
        ValueError: if nsw < 0.
    """
    if nsw < 0.0:
        raise ValueError(f"NSW must be ≥ 0; received {nsw}.")

    if abs(c) < 1e-14:
        # Wagnerowski: Sc = a·NSW + b
        # If b is not provided or 0, default to 1.0 so Sc(NSW=0) = 1.0 (physical pure water basis)
        b_eff = 1.0 if abs(b) < 1e-14 else b
        if nsw < _WAGNEROWSKI_NSW_MIN:
            warnings.warn(
                f"NSW={nsw:.4f} is below the Wagnerowski valid range "
                f"({_WAGNEROWSKI_NSW_MIN}–{_WAGNEROWSKI_NSW_MAX}). "
                "Use Vavrinecz (provide non-zero c) for low NSW solutions.",
                UserWarning,
                stacklevel=2,
            )
        elif nsw > _WAGNEROWSKI_NSW_MAX:
            warnings.warn(
                f"NSW={nsw:.4f} exceeds Wagnerowski valid range "
                f"({_WAGNEROWSKI_NSW_MIN}–{_WAGNEROWSKI_NSW_MAX}). "
                "Result may be inaccurate [NSW_OUT_OF_RANGE].",
                UserWarning,
                stacklevel=2,
            )
        return a * nsw + b_eff

    else:
        # Vavrinecz: Sc = a·NSW + b + (1 - b)·exp(c·NSW)
        return a * nsw + b + (1.0 - b) * math.exp(c * nsw)


# ---------------------------------------------------------------------------
# 4. NSW — non-sucrose to water ratio
# ---------------------------------------------------------------------------

def nsw_from_syrup(non_sucrose_1: float, water: float) -> float:
    """
    NSW from plain syrup component masses or fractions.

    NSW = NonSucrose_1 / Water   (weight basis)

    Source: Theory.md — "The non-sucrose to water ratio for any syrup is"
            RULES_v5.md §B3.4

    Args:
        non_sucrose_1: Mass (or fraction) of non-sucrose component 1.
        water:         Mass (or fraction) of water. Must be > 0 for a valid result.

    Returns:
        NSW ≥ 0.  Returns 0.0 if water == 0 (pure syrup, no impurities).

    Raises:
        ValueError: if water < 0 or non_sucrose_1 < 0.
    """
    if water < 0.0:
        raise ValueError(f"Water must be ≥ 0; received {water}.")
    if non_sucrose_1 < 0.0:
        raise ValueError(f"NonSucrose_1 must be ≥ 0; received {non_sucrose_1}.")
    if water == 0.0:
        return 0.0
    return non_sucrose_1 / water


def nsw_from_massecuite(ds_mc: float, purity_mc: float) -> float:
    """
    NSW of the mother liquor in a massecuite.

    NSW = (1 − PUmc) · DSmc / (1 − DSmc)

    Source: Theory.md — "If the flow being analyzed is a massecuite..."
            RULES_v5.md §B3.4

    Args:
        ds_mc:     Massecuite dry substance fraction (0–1). Water = 1 − ds_mc.
        purity_mc: Massecuite purity fraction (0–1). Sucrose/DS.

    Returns:
        NSW ≥ 0.

    Raises:
        ValueError: if ds_mc == 1 (no water) or inputs out of range.
    """
    if not (0.0 < ds_mc < 1.0):
        raise ValueError(
            f"ds_mc must be in (0, 1); received {ds_mc}. "
            "Pure solids (ds_mc=1) has no mother liquor."
        )
    if not (0.0 <= purity_mc <= 1.0):
        raise ValueError(f"purity_mc must be in [0, 1]; received {purity_mc}.")

    water_mc = 1.0 - ds_mc
    nsw = (1.0 - purity_mc) * ds_mc / water_mc
    return nsw


# ---------------------------------------------------------------------------
# 5. Sucrose-to-water ratio helpers
# ---------------------------------------------------------------------------

def sucrose_water_at_saturation(
    temp_c: float,
    a: float,
    b: float,
    c: float,
    nsw: float,
) -> float:
    """
    Sucrose-to-water ratio at saturation for given T and impurity composition.

    suc_water_sat = Sc(NSW, a, b, c) · S(t) / (100 − S(t))

    Source: Sugar's Help Book → Theory.md (image SucroseSolubility-6.gif)
            "(sucrose/water)_saturation = Sc · (S / (100 - S))"

    Args:
        temp_c: Temperature °C.
        a, b, c: Solubility coefficients.
        nsw:    Non-sucrose to water ratio.

    Returns:
        suc/water at saturation (dimensionless).

    Raises:
        ValueError: if S(temp_c) >= 100 (physically impossible condition).
    """
    S_pct = sucrose_saturation_pct(temp_c)         # weight-%
    Sc = saturation_coefficient(nsw, a, b, c)
    denominator = 100.0 - S_pct
    if denominator <= 0.0:
        raise ValueError(
            f"Pure saturation S = {S_pct:.4f} ≥ 100 at T={temp_c}°C: "
            "physically impossible saturation state."
        )
    return Sc * (S_pct / denominator)


# ---------------------------------------------------------------------------
# 6. Van Hook supersaturation (ICUMSA official)
# ---------------------------------------------------------------------------

def supersaturation(
    ds_ml: float,
    purity_ml: float,
    temp_c: float,
    a: float,
    b: float,
    c: float,
) -> float:
    """
    Van Hook supersaturation — ICUMSA official definition.

    Ss = (suc/water)_sample / (suc/water)_sat

    Where (suc/water)_sat is evaluated at the SAME temperature and NSW
    as the sample.

    Source: Theory.md — "Supersaturation is defined by Van Hook's expression"
            RULES_v5.md §B3.5

    Args:
        ds_ml:     Mother liquor dry substance fraction (0–1).
        purity_ml: Mother liquor purity fraction (0–1).
        temp_c:    Temperature °C.
        a, b, c:   Solubility coefficients.

    Returns:
        Ss: supersaturation ratio (dimensionless; 1.0 = exactly saturated).

    Raises:
        ValueError: if ds_ml == 1 (no water) or inputs out of range.
    """
    if not (0.0 < ds_ml < 1.0):
        raise ValueError(
            f"ds_ml must be in (0, 1); received {ds_ml}. "
            "Fully solid mother liquor has no water phase."
        )
    if not (0.0 <= purity_ml <= 1.0):
        raise ValueError(f"purity_ml must be in [0, 1]; received {purity_ml}.")

    water_ml = 1.0 - ds_ml
    sucrose_ml = purity_ml * ds_ml

    # Guard against zero-water edge case
    if water_ml < 1e-10:
        raise ValueError("Mother liquor water fraction is effectively zero.")

    # Sample sucrose-to-water ratio
    suc_water_sample = sucrose_ml / water_ml

    # NSW of mother liquor (same as massecuite NSW per Theory.md)
    nsw_ml = (1.0 - purity_ml) * ds_ml / water_ml

    # Saturation sucrose-to-water ratio at same T and NSW
    suc_water_sat = sucrose_water_at_saturation(temp_c, a, b, c, nsw_ml)

    if suc_water_sat <= 0.0:
        raise ValueError(
            f"Saturation suc/water ratio is zero or negative at T={temp_c}°C; "
            "cannot compute supersaturation."
        )

    return suc_water_sample / suc_water_sat


# ---------------------------------------------------------------------------
# Convenience: named coefficient presets
# ---------------------------------------------------------------------------

def get_preset_coefficients(preset: str) -> tuple[float, float, float]:
    """
    Return (a, b, c) for a named preset.

    Available presets:
      'BEET_GRUT'    → (0.178,  0.82, −2.1)
      'BEET_POLISH'  → (0.27,   0.71, −1.4)
      'CANE_TYPICAL' → (0.04,   0.71, −2.1)
      'WAGNEROWSKI'  → (0.036,  0.0,   0.0)

    Raises:
        KeyError: if preset is unknown.
    """
    if preset not in SATURATION_COEFFICIENTS:
        raise KeyError(
            f"Unknown preset '{preset}'. "
            f"Available: {list(SATURATION_COEFFICIENTS.keys())}"
        )
    return SATURATION_COEFFICIENTS[preset]
