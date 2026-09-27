"""
solver/schemas.py
Purity for Sugar — Pydantic Data Contracts for REST API
Schema Version: 1.0

Governed by:
  - RULES_v5.md §A12 (API Contract)
  - files (4)/PurityForSugar.bas (VBA client expectation)
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field


class FlowInitialState(BaseModel):
    mass_flow_kgh: Optional[float] = 0.0
    temperature_c: Optional[float] = 20.0
    pressure_kpa: Optional[float] = 101.325
    ds_pct: Optional[float] = 0.0
    purity_pct: Optional[float] = 0.0
    crystal_pct: Optional[float] = 0.0
    isns_pct: Optional[float] = 0.0
    gas_pct: Optional[float] = 0.0
    water: Optional[float] = 0.0
    dissolved_sucrose: Optional[float] = 0.0
    non_sucrose_1: Optional[float] = 0.0
    non_sucrose_2: Optional[float] = 0.0
    component_5: Optional[float] = 0.0
    sucrose_crystals: Optional[float] = 0.0
    fiber_isns: Optional[float] = 0.0
    cao: Optional[float] = 0.0
    caco3: Optional[float] = 0.0
    component_10: Optional[float] = 0.0
    water_vapor: Optional[float] = 0.0
    co2: Optional[float] = 0.0
    nh3: Optional[float] = 0.0
    non_condensable: Optional[float] = 0.0
    component_15: Optional[float] = 0.0
    color_icu: Optional[float] = 0.0
    sol_coef_a: Optional[float] = 0.04
    sol_coef_b: Optional[float] = 0.71
    sol_coef_c: Optional[float] = -2.1

    model_config = {"extra": "allow"}


class FlowInput(BaseModel):
    id: str
    name: Optional[str] = ""
    origin_station: Optional[Union[int, str]] = None
    dest_station: Optional[Union[int, str]] = None
    is_external: bool = False
    is_required: bool = False
    unit_cost: Optional[float] = 0.0
    unit_value: Optional[float] = 0.0
    initial_state: Dict[str, Any] = Field(default_factory=dict)


class StationInput(BaseModel):
    id: str
    page: Optional[str] = None
    station_number: int
    type: str
    name: str
    equipment_id: Optional[str] = ""
    master_name: Optional[str] = ""
    properties: Dict[str, Any] = Field(default_factory=dict)


class SolveRequest(BaseModel):
    schema_version: str = "1.0"
    model_id: Optional[str] = None
    model_name: Optional[str] = None
    units: str = "SI"
    sugar_type: str = "cane"
    convergence_tolerance: float = 0.0001
    max_iterations: int = 150
    atmospheric_pressure_kpa: float = 101.325
    solubility_mode: str = "vavrinecz"
    single_pass: bool = False
    currency_symbol: str = "$"
    campaign_days: float = 300.0
    stations: List[StationInput] = Field(default_factory=list)
    flows: List[FlowInput] = Field(default_factory=list)


class FlowRevenueItem(BaseModel):
    id: str
    name: str = ""
    mass_flow_kgh: float = 0.0
    unit_price: float = 0.0
    rate_per_hour: float = 0.0
    rate_per_day: float = 0.0
    rate_per_campaign: float = 0.0


class RevenuesSummary(BaseModel):
    currency_symbol: str = "$"
    campaign_days: float = 300.0
    total_inlet_cost_per_hour: float = 0.0
    total_inlet_cost_per_day: float = 0.0
    total_inlet_cost_per_campaign: float = 0.0
    total_outlet_revenue_per_hour: float = 0.0
    total_outlet_revenue_per_day: float = 0.0
    total_outlet_revenue_per_campaign: float = 0.0
    net_process_revenue_per_hour: float = 0.0
    net_process_revenue_per_day: float = 0.0
    net_process_revenue_per_campaign: float = 0.0
    inlet_flows: List[FlowRevenueItem] = Field(default_factory=list)
    outlet_flows: List[FlowRevenueItem] = Field(default_factory=list)


class FlowOutput(BaseModel):
    id: str
    name: Optional[str] = ""
    mass_flow_kgh: float
    temperature_c: float
    pressure_kpa: float
    tdm_pct: float
    sugar_pct: float
    ds_pct: float
    purity_pct: float
    crystal_pct: float
    isns_pct: float
    gas_pct: float
    color_icu: float
    enthalpy_kjkg: float
    density_kgm3: Optional[float] = None
    fluid_type: str
    water: float
    dissolved_sucrose: float
    non_sucrose_1: float
    non_sucrose_2: float
    component_5: Optional[float] = 0.0
    sucrose_crystals: float
    fiber_isns: float
    cao: float
    caco3: float
    component_10: Optional[float] = 0.0
    water_vapor: float
    co2: float
    nh3: float
    non_condensable: Optional[float] = 0.0
    component_15: Optional[float] = 0.0
    sol_coef_a: float
    sol_coef_b: float
    sol_coef_c: float
    unit_cost: Optional[float] = 0.0
    unit_value: Optional[float] = 0.0
    cost_per_hour: Optional[float] = 0.0
    revenue_per_hour: Optional[float] = 0.0
    cost_per_day: Optional[float] = 0.0
    revenue_per_day: Optional[float] = 0.0


class StationOutput(BaseModel):
    id: str
    station_number: int
    name: str
    type: str
    calculated_properties: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)


class SolveResponse(BaseModel):
    status: str = "converged"  # "converged", "diverged", "invalid"
    iterations: int = 0
    final_error: float = 0.0
    error_message: str = ""
    stations: List[StationOutput] = Field(default_factory=list)
    flows: List[FlowOutput] = Field(default_factory=list)
    balance_summary: Optional[Dict[str, Any]] = None
    revenues: Optional[RevenuesSummary] = None


class ValidateResponse(BaseModel):
    valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    station_count: int
    flow_count: int


class StatusResponse(BaseModel):
    status: str = "running"
    version: str = "5.0"
    engine: str = "Purity for Sugar Python Thermodynamics Engine"


class SupersaturationResponse(BaseModel):
    supersaturation: float
    saturated_sucrose_to_water: float
    saturation_coefficient: float
    dry_substance_fraction: float
    purity_fraction: float
    temperature_c: float
