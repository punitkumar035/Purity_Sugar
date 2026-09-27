"""
engine/tests/test_enthalpy.py
Validation tests for engine/enthalpy.py

Authority: Sugar's Help Book Theory.md (Heat Content section), CoolProp IAPWS-95
Calculation Register: CALC-ENT-01
Rulebook: RULES_v5.md §B7 & §B12.5
"""

import pytest
from engine.enthalpy import (
    flow_enthalpy_kJkg,
    heat_of_crystallization_kJkg,
    heat_of_dissolution_kJkg,
)


class TestPureSteamAndWaterEnthalpy:
    """
    CALC-ENT-01: Pure steam and water enthalpy benchmarks
    """

    def test_saturated_steam_100C(self):
        """CALC-ENT-01: Saturated steam at 100°C, 101.325 kPa -> 2675.6 ± 1.0 kJ/kg."""
        fractions = {"steamVapour": 1.0}
        h = flow_enthalpy_kJkg(fractions, 100.0, 101.325)
        assert abs(h - 2675.6) < 1.0, f"Steam enthalpy {h:.2f} != 2675.6 ± 1.0 kJ/kg"

    def test_saturated_liquid_water_100C(self):
        """Saturated liquid water at 100°C, 101.325 kPa -> 419.1 ± 1.0 kJ/kg."""
        fractions = {"water": 1.0}
        h = flow_enthalpy_kJkg(fractions, 99.974, 101.325)
        assert abs(h - 419.1) < 1.0

    def test_liquid_water_at_0C(self):
        """Water at reference temperature 0°C -> H ≈ 0.0 kJ/kg (< 0.2 kJ/kg accounting for 101.3 kPa compression)."""
        fractions = {"water": 1.0}
        h = flow_enthalpy_kJkg(fractions, 0.01, 101.325)
        assert abs(h - 0.0) < 0.2


class TestSugarPhaseEnthalpy:
    def test_pure_sucrose_crystal_20C(self):
        """Pure sucrose crystals at 20°C: H = Cp · T ≈ 1.288 · 20 ≈ 25.75 kJ/kg."""
        fractions = {"crystals": 1.0}
        h = flow_enthalpy_kJkg(fractions, 20.0, 101.325)
        assert abs(h - 25.75) < 0.1

    def test_thick_syrup_enthalpy(self):
        """65% Brix syrup at 60°C."""
        fractions = {
            "water": 0.35,
            "sucrose": 0.55,
            "invert": 0.05,
            "ash": 0.03,
            "ns1": 0.02,
        }
        h = flow_enthalpy_kJkg(fractions, 60.0, 101.325)
        # Cp_syrup(0.65, 60) ≈ 2.526 kJ/(kg·K) -> H ≈ 151.5 kJ/kg
        assert abs(h - 151.5) < 1.0


class TestCrystallizationHeats:
    def test_heats_of_crystallization_and_dissolution(self):
        h_cryst = heat_of_crystallization_kJkg()
        h_diss = heat_of_dissolution_kJkg()
        assert h_cryst == 54.9
        assert h_diss == -54.9
        assert h_cryst + h_diss == 0.0


class TestMultiComponentLinearity:
    def test_mixture_enthalpy_is_conservative(self):
        """50% steam + 50% water at 100°C must have H = (H_steam + H_water) / 2."""
        h_steam = flow_enthalpy_kJkg({"steamVapour": 1.0}, 100.0, 101.325)
        h_water = flow_enthalpy_kJkg({"water": 1.0}, 99.974, 101.325)

        h_mix = flow_enthalpy_kJkg({"steamVapour": 0.5, "water": 0.5}, 100.0, 101.325)
        expected = 0.5 * h_steam + 0.5 * h_water
        assert abs(h_mix - expected) < 1e-4


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
