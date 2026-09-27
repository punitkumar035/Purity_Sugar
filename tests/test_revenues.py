"""
tests/test_revenues.py
Purity for Sugar — Net Process Revenues Test Suite
Phase 04
"""

import io
import base64
import openpyxl
import pytest
from starlette.testclient import TestClient

from solver.schemas import SolveRequest, StationInput, FlowInput
from solver.network import NetworkSolver
from solver.excel_export import generate_excel_report_base64
from server.app import app


client = TestClient(app)


def test_revenues_calculation_in_network():
    req = SolveRequest(
        schema_version="1.0",
        units="SI",
        sugar_type="cane",
        currency_symbol="$",
        campaign_days=300.0,
        stations=[
            StationInput(
                id="st_evap",
                station_number=1,
                name="First Effect Evaporator",
                type="evaporator",
                properties={
                    "total_solids_pct": 65.0,
                    "sat_temperature_c": 115.0,
                },
            ),
        ],
        flows=[
            # Feed juice inlet
            FlowInput(
                id="f_juice",
                name="Clarified Juice",
                is_external=True,
                dest_station=1,
                unit_cost=0.05,  # $0.05 / kg
                initial_state={
                    "mass_flow_kgh": 100000.0,
                    "temperature_c": 98.0,
                    "pressure_kpa": 120.0,
                    "ds_pct": 13.0,
                    "purity_pct": 85.0,
                },
            ),
            # Motive steam inlet
            FlowInput(
                id="f_steam",
                name="Exhaust Steam",
                is_external=True,
                dest_station=1,
                is_required=True,
                unit_cost=0.02,  # $0.02 / kg
                initial_state={
                    "mass_flow_kgh": 0.0,
                    "temperature_c": 130.0,
                    "pressure_kpa": 270.0,
                    "water_vapor": 1.0,
                    "ds_pct": 0.0,
                },
            ),
            # Thick juice / syrup leaving
            FlowInput(
                id="f_syrup",
                name="Concentrated Syrup",
                origin_station=1,
                unit_value=0.50,  # $0.50 / kg
            ),
            # Vapor leaving
            FlowInput(
                id="f_vapor",
                name="Evaporator Vapour",
                origin_station=1,
                unit_value=0.0,
            ),
            # Condensate leaving
            FlowInput(
                id="f_cond",
                name="Steam Condensate",
                origin_station=1,
                unit_value=0.005,  # $0.005 / kg water recovery
            ),
        ],
    )

    solver = NetworkSolver(req)
    res = solver.solve()

    assert res.status == "converged"
    assert res.revenues is not None

    revs = res.revenues
    assert revs.currency_symbol == "$"
    assert revs.campaign_days == 300.0

    # Clarified juice cost: 100,000 * 0.05 = 5,000 $/h
    # Motive steam is required flow > 0 kg/h, cost > 0
    assert revs.total_inlet_cost_per_hour > 5000.0
    assert revs.total_inlet_cost_per_day > 120000.0

    # Syrup leaving: 100000 * (13/65) = 20,000 kg/h * 0.50 = 10,000 $/h
    assert revs.total_outlet_revenue_per_hour >= 9900.0
    assert revs.total_outlet_revenue_per_day >= 237600.0

    # Net process revenue must be positive and consistent
    expected_net_hr = round(revs.total_outlet_revenue_per_hour - revs.total_inlet_cost_per_hour, 2)
    assert abs(revs.net_process_revenue_per_hour - expected_net_hr) < 0.01
    expected_net_day = round(revs.total_outlet_revenue_per_day - revs.total_inlet_cost_per_day, 2)
    assert abs(revs.net_process_revenue_per_day - expected_net_day) < 0.01

    # Campaign revenue
    expected_net_camp = round(revs.total_outlet_revenue_per_campaign - revs.total_inlet_cost_per_campaign, 2)
    assert abs(revs.net_process_revenue_per_campaign - expected_net_camp) < 0.1

    # Inlet flows list
    assert len(revs.inlet_flows) >= 2
    juice_item = next(item for item in revs.inlet_flows if item.id == "f_juice")
    assert juice_item.unit_price == 0.05
    assert juice_item.rate_per_hour == 5000.0
    assert juice_item.rate_per_day == 120000.0


def test_revenues_endpoint():
    payload = {
        "schema_version": "1.0",
        "units": "SI",
        "currency_symbol": "EUR",
        "campaign_days": 120.0,
        "stations": [
            {
                "id": "st_receiver",
                "station_number": 1,
                "name": "Feed Tank",
                "type": "receiver",
                "properties": {},
            }
        ],
        "flows": [
            {
                "id": "f_in",
                "name": "Standard Liquor In",
                "is_external": True,
                "dest_station": 1,
                "unit_cost": 0.10,
                "initial_state": {
                    "mass_flow_kgh": 50000.0,
                    "temperature_c": 75.0,
                    "ds_pct": 65.0,
                    "purity_pct": 98.0,
                },
            },
            {
                "id": "f_out",
                "name": "Standard Liquor Out",
                "origin_station": 1,
                "unit_value": 0.12,
            },
        ],
    }

    resp = client.post("/revenues", json=payload)
    assert resp.status_code == 200
    data = resp.json()

    assert data["currency_symbol"] == "EUR"
    assert data["campaign_days"] == 120.0
    # 50,000 kg/h * 0.10 EUR/kg = 5,000 EUR/h
    assert data["total_inlet_cost_per_hour"] == 5000.0
    # 50,000 kg/h * 0.12 EUR/kg = 6,000 EUR/h
    assert data["total_outlet_revenue_per_hour"] == 6000.0
    # Net: 1,000 EUR/h -> 24,000 EUR/day -> 2,880,000 EUR/campaign
    assert data["net_process_revenue_per_hour"] == 1000.0
    assert data["net_process_revenue_per_day"] == 24000.0
    assert data["net_process_revenue_per_campaign"] == 2880000.0


def test_excel_export_with_revenues_worksheet():
    sim_data = {
        "status": "converged",
        "iterations": 5,
        "final_error": 0.00005,
        "stations": [
            {"station_number": 1, "name": "Mixer", "type": "receiver", "id": "st1", "calculated_properties": {}}
        ],
        "flows": [
            {
                "id": "f1",
                "name": "Sugar In",
                "mass_flow_kgh": 10000.0,
                "temperature_c": 50.0,
                "pressure_kpa": 101.325,
                "tdm_pct": 100.0,
                "sugar_pct": 99.5,
                "ds_pct": 99.5,
                "purity_pct": 99.5,
                "crystal_pct": 0.0,
                "isns_pct": 0.5,
                "gas_pct": 0.0,
                "color_icu": 50.0,
                "enthalpy_kjkg": 65.0,
                "density_kgm3": 1500.0,
                "fluid_type": "syrup",
                "water": 0.005,
                "dissolved_sucrose": 0.995,
                "non_sucrose_1": 0.0,
                "non_sucrose_2": 0.0,
                "sucrose_crystals": 0.0,
                "fiber_isns": 0.0,
                "cao": 0.0,
                "caco3": 0.0,
                "water_vapor": 0.0,
                "co2": 0.0,
                "nh3": 0.0,
                "sol_coef_a": 0.04,
                "sol_coef_b": 0.71,
                "sol_coef_c": -2.1,
            }
        ],
        "revenues": {
            "currency_symbol": "$",
            "campaign_days": 300.0,
            "total_inlet_cost_per_hour": 1500.0,
            "total_inlet_cost_per_day": 36000.0,
            "total_inlet_cost_per_campaign": 10800000.0,
            "total_outlet_revenue_per_hour": 2500.0,
            "total_outlet_revenue_per_day": 60000.0,
            "total_outlet_revenue_per_campaign": 18000000.0,
            "net_process_revenue_per_hour": 1000.0,
            "net_process_revenue_per_day": 24000.0,
            "net_process_revenue_per_campaign": 7200000.0,
            "inlet_flows": [
                {
                    "id": "f1",
                    "name": "Raw Feed",
                    "mass_flow_kgh": 10000.0,
                    "unit_price": 0.15,
                    "rate_per_hour": 1500.0,
                    "rate_per_day": 36000.0,
                    "rate_per_campaign": 10800000.0,
                }
            ],
            "outlet_flows": [
                {
                    "id": "f2",
                    "name": "Product Stream",
                    "mass_flow_kgh": 10000.0,
                    "unit_price": 0.25,
                    "rate_per_hour": 2500.0,
                    "rate_per_day": 60000.0,
                    "rate_per_campaign": 18000000.0,
                }
            ],
        },
    }

    b64_res = generate_excel_report_base64(sim_data)
    assert isinstance(b64_res, str)
    assert len(b64_res) > 500

    raw_bytes = base64.b64decode(b64_res)
    wb = openpyxl.load_workbook(io.BytesIO(raw_bytes))

    sheet_names = wb.sheetnames
    assert "Balance Summary" in sheet_names
    assert "Stream Inventory" in sheet_names
    assert "Stations Summary" in sheet_names
    assert "Process Net Revenues" in sheet_names

    ws_rev = wb["Process Net Revenues"]
    assert ws_rev["A1"].value == "PROCESS NET REVENUES REPORT"


def test_excel_download_endpoint():
    sim_data = {
        "status": "converged",
        "iterations": 2,
        "final_error": 0.00001,
        "stations": [],
        "flows": [],
    }

    resp = client.post("/export/excel/download", json=sim_data)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert "attachment" in resp.headers["content-disposition"]
    assert len(resp.content) > 500
