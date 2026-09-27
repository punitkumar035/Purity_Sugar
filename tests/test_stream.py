"""
tests/test_stream.py
Unit tests for the 15-Component Stream Model & Mixing
Phase 03
"""

import pytest
from solver.stream import Stream, mix_streams


def test_stream_default_initialization():
    s = Stream()
    assert s.mass_flow_kgh == 0.0
    assert s.temperature_c == 20.0
    assert s.pressure_kpa == 101.325
    assert abs(s.water - 1.0) < 1e-6
    assert abs(s.tdm_pct - 0.0) < 1e-4
    assert abs(s.ds_pct - 0.0) < 1e-4


def test_stream_derived_sugar_properties():
    # Pure syrup at 65 Brix, 98% purity
    ds_frac = 0.65
    purity_frac = 0.98
    sucrose_frac = ds_frac * purity_frac
    ns_frac = ds_frac - sucrose_frac
    water_frac = 1.0 - ds_frac

    s = Stream(
        mass_flow_kgh=10000.0,
        temperature_c=60.0,
        pressure_kpa=101.325,
        water=water_frac,
        dissolved_sucrose=sucrose_frac,
        non_sucrose_1=ns_frac * 0.8,
        non_sucrose_2=ns_frac * 0.2,
        sucrose_crystals=0.0,
    ).normalize()

    assert abs(s.ds_pct - 65.0) < 0.01
    assert abs(s.purity_pct - 98.0) < 0.01
    assert abs(s.crystal_pct - 0.0) < 0.01
    assert abs(s.tdm_pct - 65.0) < 0.01
    assert s.fluid_type in ("syrup", "heavy_syrup")
    assert s.enthalpy_kjkg > 100.0  # reasonable specific enthalpy
    assert s.density_kgm3 > 1200.0  # ~1300 kg/m3 for 65 Brix


def test_massecuite_properties():
    # Massecuite: 90 DS, 85 Purity, 40% Crystals
    s = Stream(
        mass_flow_kgh=5000.0,
        temperature_c=65.0,
        pressure_kpa=101.325,
        water=0.10,
        dissolved_sucrose=0.365,
        sucrose_crystals=0.40,
        non_sucrose_1=0.108,
        non_sucrose_2=0.027,
    ).normalize()

    assert abs(s.ds_pct - 90.0) < 0.05
    assert abs(s.purity_pct - 85.0) < 0.05
    assert abs(s.crystal_pct - 40.0) < 0.05
    assert s.fluid_type == "massecuite"
    assert s.density_kgm3 > 1400.0


def test_stream_wire_round_trip():
    state = {
        "mass_flow_kgh": 12500.0,
        "temperature_c": 75.0,
        "pressure_kpa": 120.0,
        "ds_pct": 68.5,
        "purity_pct": 92.0,
        "crystal_pct": 0.0,
        "color_icu": 1500.0,
    }
    s = Stream.from_initial_state(state)
    assert abs(s.mass_flow_kgh - 12500.0) < 1e-3
    assert abs(s.temperature_c - 75.0) < 1e-3
    assert abs(s.ds_pct - 68.5) < 0.1
    assert abs(s.purity_pct - 92.0) < 0.1

    wire = s.to_wire_dict("test_flow_1")
    assert wire["id"] == "test_flow_1"
    assert abs(wire["mass_flow_kgh"] - 12500.0) < 1e-3
    assert abs(wire["ds_pct"] - 68.5) < 0.1


def test_mix_streams_conservation():
    # Stream 1: Hot thin juice (10000 kg/h, 15 Brix, 85 Pur, 80°C)
    s1 = Stream.from_initial_state({
        "mass_flow_kgh": 10000.0,
        "temperature_c": 80.0,
        "pressure_kpa": 120.0,
        "ds_pct": 15.0,
        "purity_pct": 85.0,
    })

    # Stream 2: Cold thick syrup (5000 kg/h, 60 Brix, 85 Pur, 30°C)
    s2 = Stream.from_initial_state({
        "mass_flow_kgh": 5000.0,
        "temperature_c": 30.0,
        "pressure_kpa": 150.0,
        "ds_pct": 60.0,
        "purity_pct": 85.0,
    })

    mixed = mix_streams([s1, s2], pressure_mode="minimum")

    # Total mass conservation
    assert abs(mixed.mass_flow_kgh - 15000.0) < 1e-4

    # Dry substance conservation: (10000*0.15 + 5000*0.60) / 15000 = 4500 / 15000 = 0.30 (30%)
    assert abs(mixed.ds_pct - 30.0) < 0.05

    # Minimum pressure rule (§A8)
    assert mixed.pressure_kpa == 120.0

    # Temperature must be between 30°C and 80°C
    assert 30.0 < mixed.temperature_c < 80.0
