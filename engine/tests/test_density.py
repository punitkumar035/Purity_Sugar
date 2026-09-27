"""
engine/tests/test_density.py
Validation tests for engine/density.py

Authority: Sugar's Help Book Theory.md (Centrifugal_Scn-1.png), Rein Cane Sugar Eng Eq. 32.8
Calculation Register: CALC-DEN-01
Rulebook: RULES_v5.md §B8
"""

import pytest
from engine.density import (
    syrup_density_kgm3,
    massecuite_density_kgm3,
    crystal_density_kgm3,
)


class TestSyrupDensityBenchmark:
    """
    CALC-DEN-01: Syrup and Massecuite Density
    """

    def test_pure_water_limit(self):
        """At DS=0, T=20°C, density ≈ 1000 kg/m³."""
        rho = syrup_density_kgm3(0.0, 20.0)
        assert abs(rho - 1000.0) < 0.1

    def test_thick_syrup_calc_den_01(self):
        """CALC-DEN-01: DS=82.3%, T=73°C -> rho ≈ 1350 ± 50 kg/m³."""
        rho = syrup_density_kgm3(0.823, 73.0)
        assert abs(rho - 1399.0) < 5.0, f"Density {rho:.1f} kg/m³ outside expected range"

    def test_density_increases_with_brix(self):
        """Higher Brix must strictly increase density."""
        rho_15 = syrup_density_kgm3(0.15, 60.0)
        rho_50 = syrup_density_kgm3(0.50, 60.0)
        rho_70 = syrup_density_kgm3(0.70, 60.0)
        assert rho_15 < rho_50 < rho_70

    def test_density_decreases_with_temperature(self):
        """Thermal expansion lowers density at higher temperature."""
        rho_20 = syrup_density_kgm3(0.60, 20.0)
        rho_60 = syrup_density_kgm3(0.60, 60.0)
        rho_90 = syrup_density_kgm3(0.60, 90.0)
        assert rho_20 > rho_60 > rho_90


class TestMassecuiteDensityBenchmark:
    """
    Validation against Sugar's Help Book screenshot Centrifugal_Scn-1.png:
    DSmc=93.00%, PUmc=86.44%, T=81.0°C, Cry=47.44% -> Density = 1493.84 kg/m³.
    """

    def test_helpbook_centrifugal_screenshot_massecuite_density(self):
        rho_mc = massecuite_density_kgm3(
            ds_mc=0.9300,
            pu_mc=0.8644,
            crystal_frac=0.4744,
            temp_c=81.0,
        )
        assert abs(rho_mc - 1493.84) < 2.0, (
            f"Calculated massecuite density {rho_mc:.2f} kg/m³ differs from Helpbook 1493.84 kg/m³"
        )

    def test_massecuite_zero_crystals_matches_syrup(self):
        rho_mc = massecuite_density_kgm3(0.70, 0.85, 0.0, 50.0)
        rho_syr = syrup_density_kgm3(0.70, 50.0)
        assert abs(rho_mc - rho_syr) < 1e-6


class TestCrystalDensity:
    def test_sucrose_crystal_density(self):
        rho_c = crystal_density_kgm3(20.0)
        assert abs(rho_c - 1587.0) < 1.0


class TestDensityPhysicalBounds:
    def test_raises_on_invalid_ds(self):
        with pytest.raises(ValueError, match="must be in"):
            syrup_density_kgm3(-0.05, 20.0)
        with pytest.raises(ValueError, match="must be in"):
            syrup_density_kgm3(1.0, 20.0)

    def test_raises_on_invalid_crystal_frac(self):
        with pytest.raises(ValueError, match="must be in"):
            massecuite_density_kgm3(0.80, 0.85, 0.85, 60.0)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
