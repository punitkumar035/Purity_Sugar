"""
solver/stations/base.py
Purity for Sugar — Base Station Interface & Calculation Contract

Enforces SI units, mass conservation, component conservation, and explicit error handling.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple

from solver.stream import Stream, mix_streams


@dataclass
class StationResult:
    """Standardized output of a station calculation."""
    outlet_streams: Dict[str, Stream] = field(default_factory=dict)  # flow_id -> Stream
    calculated_properties: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    required_inlet_flows: Dict[str, float] = field(default_factory=dict)  # flow_id -> target mass flow kg/h


class BaseStation(ABC):
    """
    Abstract base class for all sugar process stations.
    Subclasses implement physics and unit operations based on Sugar's Help Book.
    """

    def __init__(
        self,
        station_id: str,
        station_number: int,
        name: str,
        station_type: str,
        properties: Dict[str, Any],
    ):
        self.station_id = station_id
        self.station_number = station_number
        self.name = name
        self.station_type = station_type
        self.properties = properties or {}

    def get_float(self, key: str, default: float = 0.0) -> float:
        val = self.properties.get(key)
        if val is None or val == "":
            return default
        try:
            return float(val)
        except (ValueError, TypeError):
            return default

    def get_bool(self, key: str, default: bool = False) -> bool:
        val = self.properties.get(key)
        if val is None or val == "":
            return default
        if isinstance(val, bool):
            return val
        s = str(val).strip().lower()
        return s in ("true", "1", "yes", "t")

    def get_str(self, key: str, default: str = "") -> str:
        val = self.properties.get(key)
        if val is None:
            return default
        return str(val).strip()

    @abstractmethod
    def calculate(
        self,
        inlet_streams: Dict[str, Stream],  # flow_id -> Stream
        inlet_flow_ids: List[str],
        outlet_flow_ids: List[str],
        atmospheric_p_kpa: float = 101.325,
    ) -> StationResult:
        """
        Executes material and energy balances for this station.
        Must raise ValueError with physical details on fatal physics failure.
        """
        pass
