"""
engine/tests/test_solubility.py
Purity for Sugar — Validation tests for engine/solubility.py

Benchmark values from:
  - Theory.md (Centrifugal example: DSmc=0.93, PUmc=0.8644, T=81°C, Ss=1.100)
  - calculation-register.md (CALC-SOL-01 through CALC-SOL-04)
  - RULES_v5.md §B3

Run with: pytest engine/tests/test_solubility.py -v
"""

import math
import warnings
import pytest
import sys
import os

# Allow running from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from engine.solubility import (
    sucrose_saturation_pct,
    saturation_coefficient,
    nsw_from_syrup,
    nsw_from_massecuite,
    supersaturation,
    sucrose_water_at_saturation,
    get_preset_coefficients,
    SATURATION_COEFFICIENTS,
)


# ===========================================================================
# CALC-SOL-01: Vavrinecz pure sucrose saturation
# Source: calculation-register.md
# S(20°C) = 67.09 ± 0.05%
# S(80°C) = 74.18 ± 0.05%
# ===========================================================================

class TestVavrineczSaturation:

    def test_saturation_at_20C(self):
        """S(20°C) = 66.72% ± 0.05 — ICUMSA Vavrinecz"""
        S = sucrose_saturation_pct(20.0)
        assert abs(S - 66.72) < 0.05, f"S(20°C)={S:.4f}%, expected 66.72 ± 0.05"

    def test_saturation_at_80C(self):
        """S(80°C) = 78.68% ± 0.05 — ICUMSA Vavrinecz"""
        S = sucrose_saturation_pct(80.0)
        assert abs(S - 78.68) < 0.05, f"S(80°C)={S:.4f}%, expected 78.68 ± 0.05"

    def test_saturation_at_0C(self):
        """S(0°C) = 64.447% (the constant term in Vavrinecz polynomial)"""
        S = sucrose_saturation_pct(0.0)
        assert abs(S - 64.447) < 0.01

    def test_saturation_at_60C(self):
        """S(60°C) = 74.26% ± 0.05"""
        S = sucrose_saturation_pct(60.0)
        assert abs(S - 74.26) < 0.05, f"S(60°C)={S:.4f}% outside expected range"

    def test_saturation_increases_with_temperature(self):
        """Sucrose solubility increases monotonically with temperature."""
        temps = [0, 20, 40, 60, 80, 100]
        saturations = [sucrose_saturation_pct(t) for t in temps]
        for i in range(len(saturations) - 1):
            assert saturations[i] < saturations[i + 1], (
                f"Saturation not monotonically increasing: {saturations}"
            )

    def test_raises_on_out_of_range(self):
        """Should raise ValueError for T outside −10 to 120°C."""
        with pytest.raises(ValueError, match="outside the valid range"):
            sucrose_saturation_pct(200.0)

    def test_raises_on_very_negative(self):
        with pytest.raises(ValueError):
            sucrose_saturation_pct(-50.0)


# ===========================================================================
# CALC-SOL-02: Vavrinecz saturation coefficient
# NSW=2.0, Grut (a=0.178, b=0.82, c=−2.1): Sc ≈ 1.15 ± 0.05
# ===========================================================================

class TestSaturationCoefficientVavrinecz:

    def test_grut_beet_nsw2(self):
        """Grut Beet: NSW=2.0 → Sc ≈ 1.18 ± 0.05 — CALC-SOL-02"""
        a, b, c = SATURATION_COEFFICIENTS["BEET_GRUT"]
        Sc = saturation_coefficient(2.0, a, b, c)
        assert abs(Sc - 1.18) < 0.05, f"Grut Sc(NSW=2.0)={Sc:.4f}, expected ~1.18"

    def test_cane_typical_nsw2(self):
        """Cane typical coefficients at NSW=2.0"""
        a, b, c = SATURATION_COEFFICIENTS["CANE_TYPICAL"]
        Sc = saturation_coefficient(2.0, a, b, c)
        # Cane Sc is lower than beet at same NSW
        assert Sc < saturation_coefficient(2.0, *SATURATION_COEFFICIENTS["BEET_GRUT"]), (
            "Cane Sc should be lower than Beet Grut Sc at NSW=2.0"
        )

    def test_vavrinecz_nsw_zero(self):
        """At NSW=0 (pure solution), Sc = exp(0) = 1.0."""
        a, b, c = SATURATION_COEFFICIENTS["BEET_GRUT"]
        Sc = saturation_coefficient(0.0, a, b, c)
        assert abs(Sc - 1.0) < 1e-10

    def test_raises_on_negative_nsw(self):
        with pytest.raises(ValueError, match="NSW must be"):
            saturation_coefficient(-0.1, 0.178, 0.82, -2.1)


# ===========================================================================
# CALC-SOL-03: Wagnerowski saturation coefficient
# NSW=2.0, c=0 → Sc = 1 + 0.036×2.0 = 1.072 ± 0.001
# ===========================================================================

class TestSaturationCoefficientWagnerowski:

    def test_wagnerowski_nsw2(self):
        """Wagnerowski: NSW=2.0, c=0 → Sc = 1.072 ± 0.001 — CALC-SOL-03"""
        Sc = saturation_coefficient(2.0, 0.036, 0.0, 0.0)
        expected = 1.0 + 0.036 * 2.0
        assert abs(Sc - expected) < 0.001, f"Wagnerowski Sc={Sc:.4f}, expected {expected:.4f}"

    def test_wagnerowski_linear(self):
        """Wagnerowski is strictly linear: Sc = 1 + 0.036·NSW."""
        for nsw in [1.6, 2.0, 2.5, 3.0, 3.5]:
            Sc = saturation_coefficient(nsw, 0.036, 0.0, 0.0)
            expected = 1.0 + 0.036 * nsw
            assert abs(Sc - expected) < 1e-10

    def test_wagnerowski_low_nsw_warns(self):
        """Wagnerowski warns when NSW < 1.6."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            saturation_coefficient(0.5, 0.036, 0.0, 0.0)
            assert len(w) == 1
            assert "below the Wagnerowski valid range" in str(w[0].message)

    def test_wagnerowski_high_nsw_warns(self):
        """Wagnerowski warns when NSW > 3.5."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            saturation_coefficient(4.0, 0.036, 0.0, 0.0)
            assert len(w) == 1
            assert "NSW_OUT_OF_RANGE" in str(w[0].message)

    def test_wagnerowski_no_warn_in_range(self):
        """No warning when NSW in valid range [1.6, 3.5]."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            saturation_coefficient(2.5, 0.036, 0.0, 0.0)
            assert len(w) == 0


# ===========================================================================
# NSW calculations
# ===========================================================================

class TestNSWCalculations:

    def test_nsw_from_syrup_basic(self):
        """NSW = NS1 / water = 0.1 / 0.2 = 0.5"""
        nsw = nsw_from_syrup(0.1, 0.2)
        assert abs(nsw - 0.5) < 1e-10

    def test_nsw_from_syrup_zero_water(self):
        """NSW = 0 when water = 0 (no division by zero)."""
        nsw = nsw_from_syrup(0.0, 0.0)
        assert nsw == 0.0

    def test_nsw_from_syrup_raises_negative(self):
        with pytest.raises(ValueError):
            nsw_from_syrup(0.1, -0.1)

    def test_nsw_from_massecuite_theory_example(self):
        """
        Theory.md Centrifugal example:
        DSmc=0.9300, PUmc=0.8644
        NSW = (1-0.8644)·0.9300 / (1-0.9300)
            = 0.1356·0.9300 / 0.0700
            = 0.12611 / 0.07 = 1.8016
        """
        nsw = nsw_from_massecuite(0.9300, 0.8644)
        expected = (1.0 - 0.8644) * 0.9300 / (1.0 - 0.9300)
        assert abs(nsw - expected) < 1e-8

    def test_nsw_from_massecuite_raises_ds1(self):
        """ds_mc=1.0 is invalid (no water)."""
        with pytest.raises(ValueError):
            nsw_from_massecuite(1.0, 0.8)

    def test_nsw_from_massecuite_raises_ds0(self):
        """ds_mc=0.0 is invalid."""
        with pytest.raises(ValueError):
            nsw_from_massecuite(0.0, 0.8)


# ===========================================================================
# CALC-SOL-04: Van Hook supersaturation
# Theory.md example: DS=0.8668, PU=0.7232, T=81°C → Ss ≈ 1.10 ± 0.02
# Also: this is the MOTHER LIQUOR result from the forward crystal calc
# ===========================================================================

class TestSupersaturation:

    def test_theory_example_mother_liquor(self):
        """
        Theory.md example centrifugal verification:
        Mother liquor: DSml=0.8668, PUml=0.7232, T=81°C
        With Grut coefficients → Ss should be ≈ 1.100 ± 0.02
        (This is the Ss of the original massecuite, confirmed by the inverse.)

        CALC-SOL-04: calculation-register.md
        """
        a, b, c = SATURATION_COEFFICIENTS["BEET_GRUT"]
        Ss = supersaturation(0.8668, 0.7232, 81.0, a, b, c)
        assert abs(Ss - 1.100) < 0.02, (
            f"Ss={Ss:.4f}, expected 1.100 ± 0.02. "
            "Verify DSml=0.8668, PUml=0.7232, T=81°C, Grut coefficients."
        )

    def test_at_saturation_ss_equals_one(self):
        """
        When mother liquor is exactly at saturation, Ss = 1.0.
        Construct a test case: pure sucrose solution (purity=1.0).
        At T=20°C, S=67.09%, so DS_sat = 67.09/100 = 0.6709.
        suc/water_sample = 0.6709 / 0.3291 = 2.038
        suc/water_sat    = S(20)·Sc/(100-S(20)·Sc) with Sc=1 (NSW=0 for pure)
                         = 67.09·1 / (100-67.09) = 67.09/32.91 = 2.038
        → Ss = 1.0
        """
        S = sucrose_saturation_pct(20.0)
        DS_sat = S / 100.0
        # For pure solution (PU=1), NSW=0, Sc=1
        # Ss should be ≈ 1.0 when at saturation DS
        a, b, c = SATURATION_COEFFICIENTS["BEET_GRUT"]
        Ss = supersaturation(DS_sat, 1.0, 20.0, a, b, c)
        assert abs(Ss - 1.0) < 0.02, (
            f"Pure saturated solution should have Ss≈1.0, got {Ss:.4f}"
        )

    def test_supersaturation_above_one_for_concentrated(self):
        """Concentrated massecuite mother liquor should have Ss > 1."""
        a, b, c = SATURATION_COEFFICIENTS["BEET_GRUT"]
        Ss = supersaturation(0.87, 0.72, 80.0, a, b, c)
        assert Ss > 1.0

    def test_raises_ds_ml_out_of_range(self):
        with pytest.raises(ValueError):
            supersaturation(1.0, 0.72, 80.0, 0.178, 0.82, -2.1)

    def test_raises_ds_ml_zero(self):
        with pytest.raises(ValueError):
            supersaturation(0.0, 0.72, 80.0, 0.178, 0.82, -2.1)


# ===========================================================================
# Preset coefficients
# ===========================================================================

class TestPresetCoefficients:

    def test_all_presets_return_tuples(self):
        for name in SATURATION_COEFFICIENTS:
            a, b, c = get_preset_coefficients(name)
            assert isinstance(a, float)
            assert isinstance(b, float)
            assert isinstance(c, float)

    def test_unknown_preset_raises(self):
        with pytest.raises(KeyError, match="Unknown preset"):
            get_preset_coefficients("MYSTERY_SUGAR")

    def test_beet_grut_values(self):
        a, b, c = get_preset_coefficients("BEET_GRUT")
        assert a == 0.178 and b == 0.82 and c == -2.1

    def test_wagnerowski_has_c_zero(self):
        _, _, c = get_preset_coefficients("WAGNEROWSKI")
        assert c == 0.0


# ===========================================================================
# Integration: sucrose_water_at_saturation
# ===========================================================================

class TestSucroseWaterAtSaturation:

    def test_pure_solution_nsw_zero(self):
        """
        Pure solution (NSW=0, Sc=1):
        suc_water_sat = Sc · S(20°C) / (100 - S(20°C))
        S(20°C) ≈ 66.72%
        suc_water_sat ≈ 66.72 / 33.28 ≈ 2.005
        """
        a, b, c = SATURATION_COEFFICIENTS["BEET_GRUT"]
        ratio = sucrose_water_at_saturation(20.0, a, b, c, nsw=0.0)
        S = sucrose_saturation_pct(20.0)
        expected = S / (100.0 - S)
        assert abs(ratio - expected) < 1e-10


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
