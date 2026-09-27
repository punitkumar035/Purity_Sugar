"""
tests/test_stations.py
Unit tests for all Core Unit Operations & Station Models
Phase 03
"""

import pytest
from solver.stream import Stream
from solver.stations import create_station


def test_receiver_station():
    st = create_station("receiver", "st_1", 10, "Juice Receiver", {})
    s1 = Stream.from_initial_state({"mass_flow_kgh": 1000.0, "pressure_kpa": 120.0, "ds_pct": 20.0})
    s2 = Stream.from_initial_state({"mass_flow_kgh": 2000.0, "pressure_kpa": 150.0, "ds_pct": 50.0})

    res = st.calculate(
        inlet_streams={"f1": s1, "f2": s2},
        inlet_flow_ids=["f1", "f2"],
        outlet_flow_ids=["out_1"],
    )

    out = res.outlet_streams["out_1"]
    assert abs(out.mass_flow_kgh - 3000.0) < 1e-3
    assert out.pressure_kpa == 120.0  # minimum input pressure §A8
    # DS: (1000*0.2 + 2000*0.5) / 3000 = 1200 / 3000 = 40%
    assert abs(out.ds_pct - 40.0) < 0.1


def test_distributor_station():
    st = create_station("distributor", "st_2", 20, "Juice Splitter", {
        "quantity_0": 40.0,
        "quantity_1": 60.0,
        "use_percent": True,
    })
    s_in = Stream.from_initial_state({"mass_flow_kgh": 10000.0, "ds_pct": 65.0, "temperature_c": 70.0})

    res = st.calculate(
        inlet_streams={"in_1": s_in},
        inlet_flow_ids=["in_1"],
        outlet_flow_ids=["out_1", "out_2"],
    )

    out1 = res.outlet_streams["out_1"]
    out2 = res.outlet_streams["out_2"]
    assert abs(out1.mass_flow_kgh - 4000.0) < 1e-3
    assert abs(out2.mass_flow_kgh - 6000.0) < 1e-3
    assert abs(out1.ds_pct - 65.0) < 1e-3
    assert abs(out2.ds_pct - 65.0) < 1e-3


def test_blender_station_with_ratio():
    st = create_station("blender", "st_3", 30, "Juice Blender", {"ratio": 0.25})
    s_prim = Stream.from_initial_state({"mass_flow_kgh": 4000.0, "ds_pct": 60.0})
    s_blend = Stream.from_initial_state({"mass_flow_kgh": 1000.0, "ds_pct": 20.0})

    res = st.calculate(
        inlet_streams={"f_p": s_prim, "f_b": s_blend},
        inlet_flow_ids=["f_p", "f_b"],
        outlet_flow_ids=["out_1"],
    )

    assert "f_b" in res.required_inlet_flows
    assert abs(res.required_inlet_flows["f_b"] - 1000.0) < 1e-3
    out = res.outlet_streams["out_1"]
    assert abs(out.mass_flow_kgh - 5000.0) < 1e-3


def test_flash_tank_station():
    # Hot pressurized juice entering lower pressure chamber
    st = create_station("flash_tank", "st_4", 40, "Flash Tank", {
        "vapor_pressure_kpa": 50.0,  # ~81.3°C boiling temp
    })
    s_in = Stream.from_initial_state({
        "mass_flow_kgh": 10000.0,
        "temperature_c": 105.0,  # superheated relative to 50 kPa
        "pressure_kpa": 150.0,
        "ds_pct": 15.0,
    })

    res = st.calculate(
        inlet_streams={"in_1": s_in},
        inlet_flow_ids=["in_1"],
        outlet_flow_ids=["liq_out", "vap_out"],
    )

    liq = res.outlet_streams["liq_out"]
    vap = res.outlet_streams["vap_out"]

    assert vap.mass_flow_kgh > 0.0  # vapor flashed
    assert abs(liq.mass_flow_kgh + vap.mass_flow_kgh - 10000.0) < 1e-3  # mass conservation
    # All solids remain in liquid
    assert abs(liq.mass_flow_kgh * liq.ds_fraction - 1500.0) < 1e-3
    assert liq.ds_pct > 15.0  # concentrated by flashing
    assert abs(vap.gas_pct - 100.0) < 1e-3


def test_heat_exchanger_station():
    st = create_station("heat_exchanger", "st_5", 50, "Juice Heater", {
        "temperature_out_c": 85.0,
        "port1_required": True,
    })
    s_cold = Stream.from_initial_state({"mass_flow_kgh": 20000.0, "temperature_c": 35.0, "ds_pct": 15.0})
    s_steam = Stream.from_initial_state({
        "mass_flow_kgh": 1000.0,
        "temperature_c": 120.0,
        "pressure_kpa": 200.0,
        "gas_pct": 100.0,
    })

    res = st.calculate(
        inlet_streams={"cold_in": s_cold, "steam_in": s_steam},
        inlet_flow_ids=["cold_in", "steam_in"],
        outlet_flow_ids=["cold_out", "cond_out"],
    )

    assert "steam_in" in res.required_inlet_flows
    assert res.required_inlet_flows["steam_in"] > 0.0
    cold_out = res.outlet_streams["cold_out"]
    cond_out = res.outlet_streams["cond_out"]
    assert abs(cold_out.temperature_c - 85.0) < 0.1
    assert abs(cond_out.water - 1.0) < 1e-3  # condensed to liquid water


def test_melter_station():
    st = create_station("melter", "st_6", 60, "Sugar Melter", {
        "hold_tdm_pct": 65.0,
        "temperature_out_c": 75.0,
    })
    s_sugar = Stream.from_initial_state({
        "mass_flow_kgh": 10000.0,
        "crystal_pct": 99.0,
        "ds_pct": 99.5,
        "temperature_c": 30.0,
    })
    s_dilution = Stream.from_initial_state({
        "mass_flow_kgh": 5000.0,
        "water": 1.0,
        "temperature_c": 60.0,
    })
    s_steam = Stream.from_initial_state({
        "mass_flow_kgh": 500.0,
        "temperature_c": 120.0,
        "pressure_kpa": 200.0,
        "gas_pct": 100.0,
    })

    res = st.calculate(
        inlet_streams={"sugar": s_sugar, "dilution": s_dilution, "steam": s_steam},
        inlet_flow_ids=["sugar", "dilution", "steam"],
        outlet_flow_ids=["melt_out", "cond_out"],
    )

    melt = res.outlet_streams["melt_out"]
    assert abs(melt.crystal_pct - 0.0) < 1e-3  # crystals completely dissolved §A9
    assert abs(melt.ds_pct - 65.0) < 0.5       # held at target TDM §A7
    assert melt.pressure_kpa == 101.325        # atmospheric pressure §A8


def test_evaporator_station():
    st = create_station("evaporator", "st_7", 70, "Evaporator 1st Effect", {
        "vapor_pressure_kpa": 120.0,
        "total_solids_pct": 25.0,  # concentrate from 15 to 25 Brix
    })
    s_juice = Stream.from_initial_state({
        "mass_flow_kgh": 100000.0,
        "ds_pct": 15.0,
        "purity_pct": 86.0,
        "temperature_c": 102.0,
    })
    s_steam = Stream.from_initial_state({
        "mass_flow_kgh": 40000.0,
        "temperature_c": 125.0,
        "pressure_kpa": 230.0,
        "gas_pct": 100.0,
    })

    res = st.calculate(
        inlet_streams={"juice": s_juice, "steam": s_steam},
        inlet_flow_ids=["juice", "steam"],
        outlet_flow_ids=["syrup_out", "vap_out", "cond_out"],
    )

    syrup = res.outlet_streams["syrup_out"]
    vap = res.outlet_streams["vap_out"]

    # Solids conservation: 100000 * 0.15 = 15000 kg/h DS
    # At 25 Brix, m_syrup = 15000 / 0.25 = 60000 kg/h
    assert abs(syrup.mass_flow_kgh - 60000.0) < 50.0
    assert abs(vap.mass_flow_kgh - 40000.0) < 50.0
    assert abs(syrup.ds_pct - 25.0) < 0.2
    assert "steam" in res.required_inlet_flows
    assert res.required_inlet_flows["steam"] > 0.0


def test_pan_and_crystallizer_and_centrifugal_chain():
    # 1. Vacuum Pan boiling A-massecuite
    pan = create_station("pan", "pan_1", 100, "A-Pan", {
        "vapor_pressure_kpa": 18.0,
        "total_solids_pct": 92.0,
        "supersaturation": 1.15,
    })
    syrup_feed = Stream.from_initial_state({
        "mass_flow_kgh": 50000.0,
        "ds_pct": 65.0,
        "purity_pct": 88.0,
        "temperature_c": 70.0,
    })
    pan_steam = Stream.from_initial_state({
        "mass_flow_kgh": 15000.0,
        "temperature_c": 115.0,
        "pressure_kpa": 170.0,
        "gas_pct": 100.0,
    })

    pan_res = pan.calculate(
        inlet_streams={"syrup": syrup_feed, "steam": pan_steam},
        inlet_flow_ids=["syrup", "steam"],
        outlet_flow_ids=["mc_out", "vap_out", "cond_out"],
    )

    mc = pan_res.outlet_streams["mc_out"]
    assert abs(mc.ds_pct - 92.0) < 0.5
    assert mc.crystal_pct > 35.0  # substantial crystal yield
    assert "steam" in pan_res.required_inlet_flows  # Pan steam ALWAYS required §A7

    # 2. Crystallizer cooling massecuite
    cryst = create_station("crystallizer", "cryst_1", 110, "A-Crystallizer", {
        "temperature_out_c": 45.0,
        "supersaturation": 1.05,
    })
    cryst_res = cryst.calculate(
        inlet_streams={"mc_in": mc},
        inlet_flow_ids=["mc_in"],
        outlet_flow_ids=["mc_cooled"],
    )
    mc_cooled = cryst_res.outlet_streams["mc_cooled"]
    assert mc_cooled.temperature_c == 45.0
    assert mc_cooled.crystal_pct > mc.crystal_pct  # crystals grow on cooling §A9

    # 3. Centrifugal separating crystals from molasses
    centrif = create_station("centrifugal", "centrif_1", 120, "A-Centrifugal", {
        "sugar_ds_pct": 99.2,
        "sugar_purity_pct": 99.5,
    })
    wash_water = Stream.from_initial_state({
        "mass_flow_kgh": 1000.0,
        "water": 1.0,
        "temperature_c": 80.0,
    })

    centrif_res = centrif.calculate(
        inlet_streams={"mc": mc_cooled, "wash": wash_water},
        inlet_flow_ids=["mc", "wash"],
        outlet_flow_ids=["sugar", "molasses"],
    )

    sugar = centrif_res.outlet_streams["sugar"]
    molasses = centrif_res.outlet_streams["molasses"]
    assert sugar.pressure_kpa == 101.325    # atmospheric §A8
    assert molasses.pressure_kpa == 101.325 # atmospheric §A8
    assert sugar.purity_pct > 99.0
    assert sugar.crystal_pct > 98.0
    assert molasses.purity_pct < mc_cooled.purity_pct
