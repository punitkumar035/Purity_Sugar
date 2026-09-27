"""
tests/test_network.py
Unit & Integration tests for the Flowsheet Network Solver
Phase 03
"""

import pytest
from solver.schemas import SolveRequest, StationInput, FlowInput
from solver.network import NetworkSolver


def test_single_station_receiver_network():
    req = SolveRequest(
        schema_version="1.0",
        stations=[
            StationInput(
                id="st_10",
                station_number=10,
                name="Juice Collector",
                type="receiver",
                properties={},
            )
        ],
        flows=[
            FlowInput(
                id="f_in1",
                origin_station=None,
                dest_station="st_10",
                is_external=True,
                initial_state={"mass_flow_kgh": 1000.0, "ds_pct": 15.0, "pressure_kpa": 120.0},
            ),
            FlowInput(
                id="f_in2",
                origin_station=None,
                dest_station="st_10",
                is_external=True,
                initial_state={"mass_flow_kgh": 2000.0, "ds_pct": 30.0, "pressure_kpa": 150.0},
            ),
            FlowInput(
                id="f_out",
                origin_station="st_10",
                dest_station=None,
                is_external=False,
                initial_state={},
            ),
        ],
    )

    solver = NetworkSolver(req)
    resp = solver.solve()

    assert resp.status == "converged"
    assert resp.iterations <= 2
    assert abs(resp.final_error) < 1e-4

    f_out = next(f for f in resp.flows if f.id == "f_out")
    assert abs(f_out.mass_flow_kgh - 3000.0) < 1e-3
    assert abs(f_out.ds_pct - 25.0) < 0.1
    assert f_out.pressure_kpa == 120.0  # min pressure §A8


def test_evaporator_and_heater_train_balance():
    # Cold juice -> Heater -> Evaporator
    req = SolveRequest(
        schema_version="1.0",
        stations=[
            StationInput(
                id="st_heater",
                station_number=20,
                name="Juice Preheater",
                type="heat_exchanger",
                properties={"temperature_out_c": 102.0, "port1_required": True},
            ),
            StationInput(
                id="st_evap",
                station_number=30,
                name="1st Effect Evaporator",
                type="evaporator",
                properties={"vapor_pressure_kpa": 110.0, "total_solids_pct": 30.0},
            ),
        ],
        flows=[
            # Feed juice to heater
            FlowInput(
                id="f_cold_juice",
                origin_station=None,
                dest_station="st_heater",
                is_external=True,
                initial_state={"mass_flow_kgh": 50000.0, "ds_pct": 15.0, "temperature_c": 40.0},
            ),
            # Steam to heater
            FlowInput(
                id="f_steam_heater",
                origin_station=None,
                dest_station="st_heater",
                is_external=True,
                initial_state={"mass_flow_kgh": 5000.0, "gas_pct": 100.0, "temperature_c": 130.0, "pressure_kpa": 270.0},
            ),
            # Hot juice from heater to evaporator
            FlowInput(
                id="f_hot_juice",
                origin_station="st_heater",
                dest_station="st_evap",
                is_external=False,
                initial_state={},
            ),
            # Condensate from heater
            FlowInput(
                id="f_cond_heater",
                origin_station="st_heater",
                dest_station=None,
                is_external=False,
                initial_state={},
            ),
            # Evaporator motive steam
            FlowInput(
                id="f_steam_evap",
                origin_station=None,
                dest_station="st_evap",
                is_external=True,
                initial_state={"mass_flow_kgh": 25000.0, "gas_pct": 100.0, "temperature_c": 125.0, "pressure_kpa": 230.0},
            ),
            # Evaporator syrup out
            FlowInput(
                id="f_syrup_out",
                origin_station="st_evap",
                dest_station=None,
                is_external=False,
                initial_state={},
            ),
            # Evaporator vapor out
            FlowInput(
                id="f_vap_evap",
                origin_station="st_evap",
                dest_station=None,
                is_external=False,
                initial_state={},
            ),
            # Evaporator condensate out
            FlowInput(
                id="f_cond_evap",
                origin_station="st_evap",
                dest_station=None,
                is_external=False,
                initial_state={},
            ),
        ],
    )

    solver = NetworkSolver(req)
    resp = solver.solve()

    assert resp.status == "converged"
    assert resp.iterations <= 5

    syrup_flow = next(f for f in resp.flows if f.id == "f_syrup_out")
    vap_flow = next(f for f in resp.flows if f.id == "f_vap_evap")

    # 50000 kg/h @ 15 Brix = 7500 kg/h DS
    # Concentrated to 30 Brix = 25000 kg/h syrup + 25000 kg/h vapor
    assert abs(syrup_flow.mass_flow_kgh - 25000.0) < 50.0
    assert abs(vap_flow.mass_flow_kgh - 25000.0) < 50.0
    assert abs(syrup_flow.ds_pct - 30.0) < 0.2

    # Check global balance summary
    assert resp.balance_summary is not None
    assert resp.balance_summary["ds_closure_error_pct"] < 0.05


def test_pan_crystallizer_centrifugal_melter_recycle_loop():
    """
    Tests closed recycle loop:
    Syrup Feed + Remelt Recycle -> Receiver (90)
    Receiver -> Vacuum Pan (100)
    Pan Massecuite -> Crystallizer (110)
    Crystallizer -> Centrifugal (120)
    Centrifugal Sugar (Port 0) -> Product
    Centrifugal Molasses (Port 1) -> Melter (130)
    Melter Remelt -> Receiver (90) [Tear stream recycle]
    """
    req = SolveRequest(
        schema_version="1.0",
        convergence_tolerance=0.0005,
        max_iterations=50,
        stations=[
            StationInput(
                id="st_mix",
                station_number=90,
                name="Feed & Remelt Mixer",
                type="receiver",
                properties={},
            ),
            StationInput(
                id="st_pan",
                station_number=100,
                name="A-Pan",
                type="pan",
                properties={"vapor_pressure_kpa": 18.0, "total_solids_pct": 92.0, "supersaturation": 1.15},
            ),
            StationInput(
                id="st_cryst",
                station_number=110,
                name="A-Crystallizer",
                type="crystallizer",
                properties={"temperature_out_c": 45.0, "supersaturation": 1.05},
            ),
            StationInput(
                id="st_centrif",
                station_number=120,
                name="A-Centrifugal",
                type="centrifugal",
                properties={"sugar_ds_pct": 99.2, "sugar_purity_pct": 99.5},
            ),
            StationInput(
                id="st_melt",
                station_number=130,
                name="Recycle Remelter",
                type="melter",
                properties={"hold_tdm_pct": 65.0, "temperature_out_c": 75.0},
            ),
        ],
        flows=[
            # 1. Fresh Syrup Feed to Mixer (st_mix)
            FlowInput(
                id="f_fresh_syrup",
                origin_station=None,
                dest_station="st_mix",
                is_external=True,
                initial_state={"mass_flow_kgh": 30000.0, "ds_pct": 65.0, "purity_pct": 88.0, "temperature_c": 70.0},
            ),
            # 2. Recycle Remelt from Melter to Mixer
            FlowInput(
                id="f_recycle_remelt",
                origin_station="st_melt",
                dest_station="st_mix",
                is_external=False,
                initial_state={"mass_flow_kgh": 5000.0, "ds_pct": 65.0, "purity_pct": 75.0, "temperature_c": 75.0},
            ),
            # 3. Mixed syrup to Pan
            FlowInput(
                id="f_mixed_to_pan",
                origin_station="st_mix",
                dest_station="st_pan",
                is_external=False,
                initial_state={},
            ),
            # 4. Pan steam
            FlowInput(
                id="f_pan_steam",
                origin_station=None,
                dest_station="st_pan",
                is_external=True,
                initial_state={"mass_flow_kgh": 10000.0, "gas_pct": 100.0, "temperature_c": 115.0, "pressure_kpa": 170.0},
            ),
            # 5. Pan massecuite to crystallizer
            FlowInput(
                id="f_mc_to_cryst",
                origin_station="st_pan",
                dest_station="st_cryst",
                is_external=False,
                initial_state={},
            ),
            # 6. Pan vapor
            FlowInput(
                id="f_pan_vap",
                origin_station="st_pan",
                dest_station=None,
                is_external=False,
                initial_state={},
            ),
            # 7. Pan condensate
            FlowInput(
                id="f_pan_cond",
                origin_station="st_pan",
                dest_station=None,
                is_external=False,
                initial_state={},
            ),
            # 8. Crystallizer massecuite to centrifugal
            FlowInput(
                id="f_mc_to_centrif",
                origin_station="st_cryst",
                dest_station="st_centrif",
                is_external=False,
                initial_state={},
            ),
            # 9. Centrifugal wash water
            FlowInput(
                id="f_wash_water",
                origin_station=None,
                dest_station="st_centrif",
                is_external=True,
                initial_state={"mass_flow_kgh": 1000.0, "water": 1.0, "temperature_c": 80.0},
            ),
            # 10. Centrifugal sugar to melter (fraction remelted)
            FlowInput(
                id="f_sugar_to_melt",
                origin_station="st_centrif",
                dest_station="st_melt",
                is_external=False,
                initial_state={},
            ),
            # 11. Centrifugal molasses (exits to downstream/storage)
            FlowInput(
                id="f_molasses_exit",
                origin_station="st_centrif",
                dest_station=None,
                is_external=False,
                initial_state={},
            ),
            # 12. Melter dilution sweetwater
            FlowInput(
                id="f_melt_dilution",
                origin_station=None,
                dest_station="st_melt",
                is_external=True,
                initial_state={"mass_flow_kgh": 5000.0, "water": 1.0, "temperature_c": 60.0},
            ),
            # 13. Melter heating steam
            FlowInput(
                id="f_melt_steam",
                origin_station=None,
                dest_station="st_melt",
                is_external=True,
                initial_state={"mass_flow_kgh": 500.0, "gas_pct": 100.0, "temperature_c": 120.0, "pressure_kpa": 200.0},
            ),
            # 14. Melter condensate
            FlowInput(
                id="f_melt_cond",
                origin_station="st_melt",
                dest_station=None,
                is_external=False,
                initial_state={},
            ),
        ],
    )

    solver = NetworkSolver(req)
    resp = solver.solve()

    assert resp.status == "converged"
    assert resp.iterations >= 2
    assert resp.iterations <= 50

    # Check remelt and molasses
    remelt = next(f for f in resp.flows if f.id == "f_recycle_remelt")
    molasses = next(f for f in resp.flows if f.id == "f_molasses_exit")
    assert remelt.mass_flow_kgh > 10000.0
    assert abs(remelt.ds_pct - 65.0) < 1.0  # melter held at 65 Brix
    assert molasses.mass_flow_kgh > 5000.0
    assert molasses.ds_pct > 65.0
