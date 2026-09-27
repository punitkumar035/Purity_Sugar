"""
engine/tests/test_fluids.py
Validation tests for engine/fluids.py

Authority: CoolProp (IAPWS-95 formulation for Water)
Calculation Register: CALC-ENT-01
Rulebook: RULES_v5.md §B2
"""

import pytest
from engine.fluids import (
    init_fluids,
    water_sat_temp_c,
    water_sat_pressure_kpa,
    water_enthalpy_kJkg,
    water_latent_heat_kJkg,
    water_cp_kJkgK,
    steam_is_superheated,
    steam_superheat_K,
    ethanol_water_bubble_temp_c,
)


class TestFluidsSmoke:
    def test_init_fluids_runs_cleanly(self):
        init_fluids()


class TestWaterPropertiesBenchmark:
    """
    Benchmark tests for CoolProp IAPWS-95 water/steam calculations.
    """

    def test_atmospheric_saturation_temp(self):
        """At 101.325 kPa, saturation temp is 99.974°C."""
        t_sat = water_sat_temp_c(101.325)
        assert abs(t_sat - 99.974) < 0.05

    def test_saturation_pressure_at_100C(self):
        """At 100°C, saturation pressure is ~101.42 kPa."""
        p_sat = water_sat_pressure_kpa(100.0)
        assert abs(p_sat - 101.42) < 0.1

    def test_saturated_steam_enthalpy_calc_ent_01(self):
        """CALC-ENT-01: Saturated steam at 101.325 kPa has H = 2675.6 ± 1.0 kJ/kg."""
        h_vap = water_enthalpy_kJkg(100.0, 101.325, quality=1.0)
        assert abs(h_vap - 2675.6) < 1.0, f"H_vap={h_vap:.2f}, expected 2675.6 ± 1.0 kJ/kg"

    def test_saturated_liquid_enthalpy_atmospheric(self):
        """Saturated liquid water at 101.325 kPa has H ≈ 419.06 ± 1.0 kJ/kg."""
        h_liq = water_enthalpy_kJkg(99.974, 101.325, quality=0.0)
        assert abs(h_liq - 419.06) < 1.0

    def test_water_latent_heat_at_100C(self):
        """Latent heat of vaporisation at 100°C is ~2256.5 kJ/kg."""
        latent = water_latent_heat_kJkg(100.0)
        assert abs(latent - 2256.5) < 2.0

    def test_water_cp_at_20C(self):
        """Specific heat of liquid water at 20°C is ~4.184 kJ/(kg·K)."""
        cp = water_cp_kJkgK(20.0, 101.325)
        assert abs(cp - 4.184) < 0.02


class TestSteamSuperheat:
    def test_superheat_detection(self):
        """150°C at 101.325 kPa is superheated by ~50.03 K."""
        assert steam_is_superheated(150.0, 101.325) is True
        dt = steam_superheat_K(150.0, 101.325)
        assert abs(dt - 50.03) < 0.1

    def test_not_superheated(self):
        """80°C at 101.325 kPa is not superheated."""
        assert steam_is_superheated(80.0, 101.325) is False
        assert steam_superheat_K(80.0, 101.325) == 0.0


class TestEthanolWaterMixture:
    def test_pure_water_limit(self):
        t = ethanol_water_bubble_temp_c(0.0, 101.325)
        assert abs(t - 99.974) < 0.05

    def test_pure_ethanol_limit(self):
        t = ethanol_water_bubble_temp_c(1.0, 101.325)
        # Boiling point of pure ethanol at atmospheric pressure is ~78.3°C
        assert abs(t - 78.3) < 0.5

    def test_mixture_bubble_point(self):
        t = ethanol_water_bubble_temp_c(0.5, 101.325)
        # Bubble point of 50 mol% ethanol-water is between 78°C and 85°C
        assert 75.0 < t < 86.0


class TestFluidsPhysicalBounds:
    def test_raises_on_non_positive_pressure(self):
        with pytest.raises(ValueError, match="Pressure must be > 0"):
            water_sat_temp_c(-10.0)

    def test_raises_on_invalid_temp(self):
        with pytest.raises(ValueError, match="outside valid saturation range"):
            water_sat_pressure_kpa(-50.0)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
