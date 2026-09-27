"""
tests/test_server.py
Integration tests for the FastAPI Server Endpoints
Phase 03
"""

import base64
import pytest
from starlette.testclient import TestClient
from server.app import app

client = TestClient(app)


def test_status_endpoint():
    resp = client.get("/status")
    assert resp.status_code == 200
    data = resp.json()
    # PurityForSugar.bas EngineIsRunning() specifically checks:
    # EngineIsRunning = (r <> "" And InStr(LCase(r), "running") > 0)
    assert "running" in data["status"].lower()
    assert data["version"] == "5.0"


def test_supersaturation_endpoint():
    # DS=86.68%, Purity=72.32%, T=81°C, Polish/Grut beet: Ss ~ 1.10
    resp = client.get("/supersaturation?ds=86.68&purity=72.32&temp=81.0&a=0.178&b=0.82&c=-2.1")
    assert resp.status_code == 200
    data = resp.json()
    assert abs(data["supersaturation"] - 1.10) < 0.05
    assert data["saturated_sucrose_to_water"] > 0.0
    assert data["saturation_coefficient"] > 0.0


def test_validate_endpoint():
    # Model with duplicate station numbers
    bad_req = {
        "schema_version": "1.0",
        "stations": [
            {"id": "s1", "station_number": 10, "type": "receiver", "name": "Receiver 1"},
            {"id": "s2", "station_number": 10, "type": "tank", "name": "Receiver 2"},
        ],
        "flows": [],
    }
    resp = client.post("/validate", json=bad_req)
    assert resp.status_code == 200
    data = resp.json()
    assert data["valid"] is False
    assert len(data["errors"]) > 0

    # Model with valid station numbers
    good_req = {
        "schema_version": "1.0",
        "stations": [
            {"id": "s1", "station_number": 10, "type": "receiver", "name": "Receiver 1"},
            {"id": "s2", "station_number": 20, "type": "tank", "name": "Receiver 2"},
        ],
        "flows": [],
    }
    resp = client.post("/validate", json=good_req)
    assert resp.status_code == 200
    data = resp.json()
    assert data["valid"] is True
    assert len(data["errors"]) == 0


def test_solve_endpoint_always_200():
    # Solves simple receiver
    req = {
        "schema_version": "1.0",
        "stations": [
            {"id": "s10", "station_number": 10, "type": "receiver", "name": "Main Mixer", "properties": {}}
        ],
        "flows": [
            {
                "id": "f1",
                "origin_station": None,
                "dest_station": "s10",
                "is_external": True,
                "initial_state": {"mass_flow_kgh": 1000.0, "ds_pct": 20.0},
            },
            {
                "id": "f_out",
                "origin_station": "s10",
                "dest_station": None,
                "is_external": False,
                "initial_state": {},
            },
        ],
    }

    # CRITICAL: HTTP 200 for all solver outcomes (RULES_v5.md §A12)
    resp = client.post("/solve", json=req)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "converged"
    assert data["iterations"] >= 1
    assert len(data["flows"]) == 2
    f_out = next(f for f in data["flows"] if f["id"] == "f_out")
    assert abs(f_out["mass_flow_kgh"] - 1000.0) < 1e-3
    assert abs(f_out["ds_pct"] - 20.0) < 0.1


def test_excel_export_endpoint():
    sample_results = {
        "status": "converged",
        "iterations": 3,
        "final_error": 0.000012,
        "stations": [
            {"id": "st_1", "station_number": 10, "name": "Evaporator", "type": "evaporator", "calculated_properties": {"syrup_brix": 65.0}}
        ],
        "flows": [
            {
                "id": "flow_101",
                "mass_flow_kgh": 50000.0,
                "temperature_c": 75.0,
                "pressure_kpa": 101.3,
                "ds_pct": 65.0,
                "purity_pct": 88.0,
                "crystal_pct": 0.0,
                "tdm_pct": 65.0,
                "enthalpy_kjkg": 250.0,
                "fluid_type": "syrup",
                "water": 0.35,
                "dissolved_sucrose": 0.572,
                "non_sucrose_1": 0.078,
                "non_sucrose_2": 0.0,
                "sucrose_crystals": 0.0,
                "color_icu": 3500.0,
            }
        ],
        "balance_summary": {
            "total_mass_in_kgh": 50000.0,
            "total_mass_out_kgh": 50000.0,
            "mass_closure_error_pct": 0.0,
            "total_ds_in_kgh": 32500.0,
            "total_ds_out_kgh": 32500.0,
            "ds_closure_error_pct": 0.0,
        },
    }

    resp = client.post("/export/excel", json=sample_results)
    assert resp.status_code == 200
    b64_content = resp.text
    assert len(b64_content) > 100

    # Verify that it decodes to a valid zip/xlsx file (starts with PK\x03\x04)
    file_bytes = base64.b64decode(b64_content)
    assert file_bytes[:2] == b"PK"
