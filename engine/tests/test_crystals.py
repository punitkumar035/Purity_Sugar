"""
engine/tests/test_crystals.py
Validation tests for engine/crystals.py

Authority: Sugar's Help Book Theory.md (Crystal Content & Centrifugal evaluation)
Reference Screenshot: Centrifugal_Scn-1.png
Calculation Register: CALC-CRY-01, CALC-CRY-02
Rulebook: RULES_v5.md §B4 & §B12.2
"""

import pytest
from engine.crystals import (
    crystals_forward,
    crystals_inverse,
    massecuite_crystal_content,
)
from engine.solubility import SATURATION_COEFFICIENTS


class TestCrystalsForwardBenchmark:
    """
    Benchmark test from Sugar's Help Book Theory.md and Centrifugal_Scn-1.png:
    Massecuite: DSmc=0.9300, PUmc=0.8644, T=81.0°C, Ss=1.100, Beet Grut (0.178, 0.82, -2.1)
    """

    def test_theory_helpbook_benchmark(self):
        a, b, c = SATURATION_COEFFICIENTS["BEET_GRUT"]
        res = crystals_forward(
            ds_mc=0.9300,
            pu_mc=0.8644,
            temp_c=81.0,
            ss=1.100,
            a=a,
            b=b,
            c=c,
        )

        # 1. Crystal content: 47.44 wt% (Cry = 0.4744)
        assert abs(res["crystal_frac"] - 0.4744) < 0.001, (
            f"Crystal fraction {res['crystal_frac']:.4f} != expected 0.4744"
        )

        # 2. Mother liquor DS: 86.68% (DSml = 0.8668)
        assert abs(res["ds_ml"] - 0.8668) < 0.001, (
            f"Mother liquor DS {res['ds_ml']:.4f} != expected 0.8668"
        )

        # 3. Mother liquor purity: 72.32% (PUml = 0.7232)
        assert abs(res["pu_ml"] - 0.7232) < 0.001, (
            f"Mother liquor purity {res['pu_ml']:.4f} != expected 0.7232"
        )

        # 4. Non-sucrose to water ratio: 1.8015
        assert abs(res["nsw"] - 1.8015) < 0.001, (
            f"NSW {res['nsw']:.4f} != expected 1.8015"
        )

        # 5. Cross-check supersaturation matches requested 1.100
        assert abs(res["ss_calc"] - 1.100) < 0.002, (
            f"Calculated Ss {res['ss_calc']:.4f} != expected 1.100"
        )

    def test_convenience_massecuite_crystal_content(self):
        a, b, c = SATURATION_COEFFICIENTS["BEET_GRUT"]
        cry = massecuite_crystal_content(0.9300, 0.8644, 81.0, 1.100, a, b, c)
        assert abs(cry - 0.4744) < 0.001


class TestCrystalsInverseBenchmark:
    """
    Inverse calculation: given DSmc=0.9300, PUmc=0.8644, Cry=0.4744 → recover DSml and PUml.
    """

    def test_inverse_recovery(self):
        res = crystals_inverse(ds_mc=0.9300, pu_mc=0.8644, crystal_frac=0.4744)
        assert abs(res["ds_ml"] - 0.8668) < 0.001
        assert abs(res["pu_ml"] - 0.7232) < 0.001

    def test_round_trip_exactness(self):
        """
        Forward then inverse should recover exact DSml and PUml within numerical epsilon.
        """
        a, b, c = SATURATION_COEFFICIENTS["BEET_GRUT"]
        fwd = crystals_forward(0.9300, 0.8644, 81.0, 1.100, a, b, c)
        inv = crystals_inverse(0.9300, 0.8644, fwd["crystal_frac"])

        assert abs(fwd["ds_ml"] - inv["ds_ml"]) < 1e-12
        assert abs(fwd["pu_ml"] - inv["pu_ml"]) < 1e-12


class TestCrystalsMassConservation:
    """
    Verify fundamental mass conservation across forward calculation:
    - Dry substance closure
    - Sucrose closure
    - Water closure
    - Non-sucrose closure
    """

    def test_mass_balances_theory_example(self):
        a, b, c = SATURATION_COEFFICIENTS["BEET_GRUT"]
        ds_mc = 0.9300
        pu_mc = 0.8644
        res = crystals_forward(ds_mc, pu_mc, 81.0, 1.100, a, b, c)

        cry = res["crystal_frac"]
        ds_ml = res["ds_ml"]
        pu_ml = res["pu_ml"]
        w_ml = 1.0 - cry

        # Dry substance closure: DSmc = Cry·1 + Wml·DSml
        ds_reconstituted = cry * 1.0 + w_ml * ds_ml
        assert abs(ds_mc - ds_reconstituted) < 1e-12, "Dry substance balance failed"

        # Sucrose closure: DSmc·PUmc = Cry·1 + Wml·DSml·PUml
        suc_mc = ds_mc * pu_mc
        suc_reconstituted = cry * 1.0 + w_ml * ds_ml * pu_ml
        assert abs(suc_mc - suc_reconstituted) < 1e-12, "Sucrose balance failed"

        # Water closure: (1 - DSmc) = Wml·(1 - DSml)
        water_mc = 1.0 - ds_mc
        water_reconstituted = w_ml * (1.0 - ds_ml)
        assert abs(water_mc - water_reconstituted) < 1e-12, "Water balance failed"

        # Non-sucrose closure: DSmc·(1 - PUmc) = Wml·DSml·(1 - PUml)
        ns_mc = ds_mc * (1.0 - pu_mc)
        ns_reconstituted = w_ml * ds_ml * (1.0 - pu_ml)
        assert abs(ns_mc - ns_reconstituted) < 1e-12, "Non-sucrose balance failed"


class TestCrystalsEdgeCasesAndValidation:
    """
    Physical bounds checking and exception handling.
    """

    def test_raises_on_invalid_ds_mc(self):
        a, b, c = SATURATION_COEFFICIENTS["BEET_GRUT"]
        with pytest.raises(ValueError, match="Massecuite DS must be in"):
            crystals_forward(0.0, 0.85, 80.0, 1.1, a, b, c)
        with pytest.raises(ValueError, match="Massecuite DS must be in"):
            crystals_forward(1.0, 0.85, 80.0, 1.1, a, b, c)
        with pytest.raises(ValueError, match="Massecuite DS must be in"):
            crystals_forward(1.2, 0.85, 80.0, 1.1, a, b, c)

    def test_raises_on_invalid_pu_mc(self):
        a, b, c = SATURATION_COEFFICIENTS["BEET_GRUT"]
        with pytest.raises(ValueError, match="Massecuite purity must be in"):
            crystals_forward(0.9, 0.0, 80.0, 1.1, a, b, c)
        with pytest.raises(ValueError, match="Massecuite purity must be in"):
            crystals_forward(0.9, 1.05, 80.0, 1.1, a, b, c)

    def test_raises_on_negative_ss(self):
        a, b, c = SATURATION_COEFFICIENTS["BEET_GRUT"]
        with pytest.raises(ValueError, match="Supersaturation must be > 0"):
            crystals_forward(0.9, 0.85, 80.0, -1.0, a, b, c)
        with pytest.raises(ValueError, match="Supersaturation must be > 0"):
            crystals_forward(0.9, 0.85, 80.0, 0.0, a, b, c)

    def test_inverse_raises_on_crystal_exceeding_ds(self):
        with pytest.raises(ValueError, match="must be in"):
            crystals_inverse(ds_mc=0.80, pu_mc=0.85, crystal_frac=0.85)

    def test_inverse_raises_on_negative_crystal(self):
        with pytest.raises(ValueError, match="must be in"):
            crystals_inverse(ds_mc=0.80, pu_mc=0.85, crystal_frac=-0.05)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
