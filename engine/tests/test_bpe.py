"""
engine/tests/test_bpe.py
Validation tests for engine/bpe.py

Authority: Sugar's Help Book Theory.md (Boiling Point Elevation section), KBD (1978)
Calculation Register: CALC-BPE-01
Rulebook: RULES_v5.md §B6 & §B12.3
"""

import pytest
from engine.bpe import (
    bpe_celsius,
    bpe_bubnik_kadlec,
    bpe_kbd_1978_pure,
    boiling_temp_c,
    vapor_sat_temp_from_boiling,
    pressure_from_vapor_temp,
)
from engine.fluids import water_sat_temp_c


class TestBPEPureWaterLimit:
    """
    CALC-BPE-01: Pure water (DS=0) must have BPE = 0.0 °C.
    """

    def test_ds_zero_gives_zero_bpe(self):
        bpe = bpe_celsius(0.0, 0.85, 101.325)
        assert bpe == 0.0

    def test_ds_zero_boiling_temp_equals_tsat(self):
        t_boil = boiling_temp_c(0.0, 0.85, 101.325)
        t_sat = water_sat_temp_c(101.325)
        assert abs(t_boil - t_sat) < 1e-6


class TestBPEEvaporatorAndSyrupRanges:
    """
    Typical factory juice and syrup ranges.
    """

    def test_clarified_juice_low_bpe(self):
        """Clarified juice (~15% DS) has low BPE (< 0.5°C)."""
        bpe = bpe_celsius(0.15, 0.85, 101.325)
        assert 0.05 < bpe < 0.50

    def test_evaporator_thick_juice_bpe(self):
        """Syrup at 65% DS has BPE between 2.5°C and 4.5°C."""
        bpe = bpe_celsius(0.65, 0.85, 50.0)
        assert 2.5 < bpe < 4.5

    def test_bpe_increases_with_ds(self):
        """BPE must strictly increase as concentration increases."""
        bpe_15 = bpe_celsius(0.15, 0.85, 101.325)
        bpe_40 = bpe_celsius(0.40, 0.85, 101.325)
        bpe_65 = bpe_celsius(0.65, 0.85, 101.325)
        bpe_75 = bpe_celsius(0.75, 0.85, 101.325)
        assert bpe_15 < bpe_40 < bpe_65 < bpe_75


class TestBPEFactorMultiplier:
    """
    RULES_v5.md §B6.2: BPE_effective = BPE × BPEFactor
    """

    def test_bpe_factor_scaling(self):
        t_sat = water_sat_temp_c(101.325)
        bpe = bpe_celsius(0.60, 0.85, 101.325)
        t_boil_1 = boiling_temp_c(0.60, 0.85, 101.325, bpe_factor=1.0)
        t_boil_12 = boiling_temp_c(0.60, 0.85, 101.325, bpe_factor=1.2)

        assert abs(t_boil_1 - (t_sat + bpe)) < 1e-6
        assert abs(t_boil_12 - (t_sat + bpe * 1.2)) < 1e-6


class TestVaporTempInverseSolver:
    """
    Inverse: recover T_sat from known T_boil.
    """

    def test_inverse_recovery(self):
        ds = 0.60
        pu = 0.85
        p = 60.0
        t_sat_expected = water_sat_temp_c(p)
        t_boil = boiling_temp_c(ds, pu, p)

        t_sat_recovered = vapor_sat_temp_from_boiling(t_boil, ds, pu)
        assert abs(t_sat_recovered - t_sat_expected) < 0.01


class TestKBDPureSucroseModel:
    """
    Kadlec, Bretschneider and Dandor (1978) formulation.
    """

    def test_kbd_pure_sucrose_at_zero(self):
        assert bpe_kbd_1978_pure(101.325, 0.0) == 0.0

    def test_kbd_pure_sucrose_positive(self):
        bpe = bpe_kbd_1978_pure(101.325, 0.50)
        assert 1.0 < bpe < 3.0


class TestBPEPhysicalBounds:
    def test_raises_on_invalid_ds(self):
        with pytest.raises(ValueError, match="outside physical range"):
            bpe_bubnik_kadlec(1.10, 0.85, 100.0)

    def test_raises_on_invalid_purity(self):
        with pytest.raises(ValueError, match="must be in"):
            bpe_bubnik_kadlec(0.60, 1.20, 100.0)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
