"""
engine/tests/test_heat_content.py
Validation tests for engine/heat_content.py

Authority: Sugar Technologists Manual (Bartens 8th ed), Boynton, Vukov
Calculation Register: CALC-CP-01, CALC-CP-02
Rulebook: RULES_v5.md §B5 & §B12.4
"""

import pytest
from engine.heat_content import (
    cp_syrup,
    cp_sucrose_crystal,
    cp_water_liquid,
    cp_water_vapor,
    cp_caco3,
    cp_cao,
    cp_ca_oh2,
    cp_fiber,
    cp_co2_gas,
    cp_nh3_gas,
)


class TestSyrupSpecificHeat:
    """
    CALC-CP-01: Sugar Technologists Manual eq 341/3
    """

    def test_pure_water_limit_zero_deg(self):
        """At DS=0, t=0°C, Cp = 4.187 kJ/(kg·K)."""
        cp = cp_syrup(0.0, 0.0)
        assert abs(cp - 4.187) < 0.001

    def test_pure_water_at_20C(self):
        """At DS=0, t=20°C, Cp = 4.308 ± 0.01 kJ/(kg·K)."""
        cp = cp_syrup(0.0, 20.0)
        expected = 4.187 + 0.00604 * 20.0
        assert abs(cp - expected) < 0.001

    def test_thick_juice_typical_state(self):
        """Thick juice DS=65%, 60°C has Cp ≈ 2.53 kJ/(kg·K)."""
        cp = cp_syrup(0.65, 60.0)
        assert abs(cp - 2.526) < 0.01

    def test_cp_decreases_with_increasing_ds(self):
        """Higher dry solids must strictly lower syrup specific heat."""
        cp_low = cp_syrup(0.15, 50.0)
        cp_mid = cp_syrup(0.50, 50.0)
        cp_high = cp_syrup(0.85, 50.0)
        assert cp_low > cp_mid > cp_high

    def test_raises_on_invalid_ds(self):
        with pytest.raises(ValueError, match="must be in"):
            cp_syrup(-0.1, 50.0)
        with pytest.raises(ValueError, match="must be in"):
            cp_syrup(1.1, 50.0)


class TestSucroseCrystalSpecificHeat:
    """
    CALC-CP-02: Sugar Technologists Manual eq 311/2
    """

    def test_crystal_cp_at_20C(self):
        """CALC-CP-02: t=20°C -> Cp = 1.288 ± 0.005 kJ/(kg·K)."""
        cp = cp_sucrose_crystal(20.0)
        assert abs(cp - 1.288) < 0.005, f"Cp={cp:.4f}, expected 1.288"

    def test_crystal_cp_at_60C(self):
        """t=60°C -> Cp ≈ 1.359 kJ/(kg·K)."""
        cp = cp_sucrose_crystal(60.0)
        assert abs(cp - 1.359) < 0.01


class TestMineralAndGasSpecificHeat:
    """
    Boynton, Vukov, and Chemical Engineering formulas.
    """

    def test_caco3_boynton(self):
        cp = cp_caco3(20.0)
        assert 0.50 < cp < 0.70

    def test_cao_boynton(self):
        cp = cp_cao(20.0)
        assert 0.55 < cp < 0.75

    def test_ca_oh2_constant(self):
        assert abs(cp_ca_oh2(50.0) - 1.30) < 1e-6

    def test_fiber_vukov(self):
        # Bone dry fiber (moisture=0)
        assert abs(cp_fiber(20.0, 0.0) - 1.25) < 1e-6
        # 50% moisture bagasse
        assert abs(cp_fiber(20.0, 0.50) - 1.42) < 1e-6

    def test_co2_gas(self):
        cp = cp_co2_gas(25.0)
        assert 0.80 < cp < 0.90

    def test_nh3_gas(self):
        cp = cp_nh3_gas(25.0)
        assert 2.00 < cp < 2.30

    def test_water_liquid_and_vapor_via_coolprop(self):
        cp_liq = cp_water_liquid(20.0, 101.325)
        assert abs(cp_liq - 4.184) < 0.02
        cp_vap = cp_water_vapor(150.0, 101.325)
        assert 1.80 < cp_vap < 2.20


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
