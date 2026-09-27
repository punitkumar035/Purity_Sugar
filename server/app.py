"""
server/app.py
Purity for Sugar — FastAPI Balance Solver & Thermodynamics Service
Listening on http://localhost:8765

Governed by:
  - RULES_v5.md §A12 (API Contract)
  - files (4)/PurityForSugar.bas (Visio Foundation VBA Client)
"""

from __future__ import annotations
import json
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request, Query, Response
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from solver.schemas import (
    SolveRequest,
    SolveResponse,
    ValidateResponse,
    StatusResponse,
    SupersaturationResponse,
    RevenuesSummary,
)
from solver.network import NetworkSolver
from solver.excel_export import generate_excel_report_base64
from engine.solubility import supersaturation, saturation_coefficient, sucrose_water_at_saturation

app = FastAPI(
    title="Purity for Sugar Engine",
    description="Python Network Balance Solver & Sugar Thermodynamics API",
    version="5.0",
)

# Enable CORS for browser-based simulation frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/status", response_model=StatusResponse)
async def get_status() -> Dict[str, Any]:
    """
    Returns engine health status.
    VBA EngineIsRunning() specifically checks for the substring 'running' (RULES_v5.md §A12).
    """
    return {
        "status": "running",
        "version": "5.0",
        "engine": "Purity for Sugar Python Thermodynamics Engine",
    }


@app.post("/solve", response_model=SolveResponse)
async def solve_balance(request: SolveRequest) -> SolveResponse:
    """
    Executes full mass and energy network balance for the complete flowsheet graph.
    Always returns HTTP 200 with solver status ('converged', 'diverged', or 'invalid').
    """
    solver = NetworkSolver(request)
    result = solver.solve()
    return result


@app.post("/validate", response_model=ValidateResponse)
async def validate_model(request: SolveRequest) -> ValidateResponse:
    """
    Performs topology and property consistency pre-checks without solving.
    """
    errors = []
    warnings = []

    used_numbers = set()
    for st in request.stations:
        if st.station_number <= 0:
            errors.append(f"Station '{st.name}' has invalid station number {st.station_number} (must be 1–9999).")
        elif st.station_number in used_numbers:
            errors.append(f"Duplicate station number {st.station_number} on '{st.name}'.")
        used_numbers.add(st.station_number)

        if not st.name or not st.name.strip():
            warnings.append(f"Station {st.station_number} has an empty name.")

    # Check flow connectivity
    station_ids = {st.id for st in request.stations}
    station_ids.update(str(st.station_number) for st in request.stations)

    for f in request.flows:
        if f.origin_station and str(f.origin_station).strip() not in ("", "0"):
            if str(f.origin_station).strip() not in station_ids:
                warnings.append(f"Flow {f.id} has unknown origin station '{f.origin_station}'.")
        if f.dest_station and str(f.dest_station).strip() not in ("", "0"):
            if str(f.dest_station).strip() not in station_ids:
                warnings.append(f"Flow {f.id} has unknown destination station '{f.dest_station}'.")

    is_valid = len(errors) == 0

    return ValidateResponse(
        valid=is_valid,
        errors=errors,
        warnings=warnings,
        station_count=len(request.stations),
        flow_count=len(request.flows),
    )


@app.post("/revenues", response_model=RevenuesSummary)
async def calculate_revenues(request: SolveRequest) -> RevenuesSummary:
    """
    Calculates process net revenues for the given flowsheet model.
    Runs the network balance and returns the detailed inlet costs, product revenues, and net profits.
    """
    solver = NetworkSolver(request)
    result = solver.solve()
    return result.revenues or RevenuesSummary(currency_symbol=request.currency_symbol, campaign_days=request.campaign_days)


@app.post("/export/excel")
async def export_excel(request: Request) -> Response:
    """
    Generates an Excel workbook from simulation results and returns raw base64 string.
    VBA Base64Decode directly decodes the response text (RULES_v5.md §A12).
    """
    body = await request.body()
    body_text = body.decode("utf-8", errors="replace")

    b64_str = generate_excel_report_base64(body_text)
    return PlainTextResponse(content=b64_str, media_type="text/plain")


@app.post("/export/excel/download")
async def export_excel_download(request: Request) -> Response:
    """
    Directly returns the .xlsx binary file for browser download.
    """
    import base64
    body = await request.body()
    body_text = body.decode("utf-8", errors="replace")
    b64_str = generate_excel_report_base64(body_text)
    excel_bytes = base64.b64decode(b64_str)
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=Purity_Sugar_Balance_Report.xlsx"},
    )


@app.get("/supersaturation", response_model=SupersaturationResponse)
async def get_supersaturation(
    ds: float = Query(..., description="Dry substance (fraction 0-1 or percentage 0-100)"),
    purity: float = Query(..., description="Purity (fraction 0-1 or percentage 0-100)"),
    temp: float = Query(..., description="Temperature in °C"),
    a: float = Query(0.04, description="Solubility coefficient a"),
    b: float = Query(0.71, description="Solubility coefficient b"),
    c: float = Query(-2.1, description="Solubility coefficient c"),
) -> SupersaturationResponse:
    """
    Calculates supersaturation (Ss), saturation coefficient (Sc), and saturated sucrose/water ratio.
    """
    # Normalize fractions if passed as percentages
    ds_frac = ds / 100.0 if ds > 1.0 else ds
    purity_frac = purity / 100.0 if purity > 1.0 else purity

    ss_val = supersaturation(ds_frac, purity_frac, temp, a, b, c)

    nsw = ((1.0 - purity_frac) * ds_frac) / max(1e-9, 1.0 - ds_frac)
    sc_val = saturation_coefficient(nsw, a, b, c)
    sat_ratio = sucrose_water_at_saturation(temp, a, b, c, nsw)

    return SupersaturationResponse(
        supersaturation=round(ss_val, 4),
        saturated_sucrose_to_water=round(sat_ratio, 4),
        saturation_coefficient=round(sc_val, 4),
        dry_substance_fraction=round(ds_frac, 6),
        purity_fraction=round(purity_frac, 6),
        temperature_c=temp,
    )
