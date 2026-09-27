"""
solver/stations/__init__.py
Purity for Sugar — Station Registry and Factory
Phase 03
"""

from typing import Dict, Any, Type

from solver.stations.base import BaseStation, StationResult
from solver.stations.receiver import ReceiverStation
from solver.stations.distributor import DistributorStation
from solver.stations.blender import BlenderStation
from solver.stations.flash_tank import FlashTankStation
from solver.stations.heat_exchanger import HeatExchangerStation
from solver.stations.injection_heater import InjectionHeaterStation
from solver.stations.cooler import CoolerStation
from solver.stations.tank import TankStation
from solver.stations.melter import MelterStation
from solver.stations.evaporator import EvaporatorStation
from solver.stations.pan import PanStation
from solver.stations.crystallizer import CrystallizerStation
from solver.stations.centrifugal import CentrifugalStation
from solver.stations.pump import PumpStation
from solver.stations.pressure_reducer import PressureReducerStation
from solver.stations.turbine import TurbineStation
from solver.stations.turbo_alternator import TurboAlternatorStation
from solver.stations.thermocompressor import ThermocompressorStation
from solver.stations.compressor import CompressorStation
from solver.stations.condensers import ContactCondenserStation, SurfaceCondenserStation
from solver.stations.process_units import ReactorStation, SeparatorFilterStation, DryerStation

STATION_REGISTRY: Dict[str, Type[BaseStation]] = {
    "receiver": ReceiverStation,
    "distributor": DistributorStation,
    "blender": BlenderStation,
    "flash_tank": FlashTankStation,
    "heat_exchanger": HeatExchangerStation,
    "injection_heater": InjectionHeaterStation,
    "cooler": CoolerStation,
    "tank": TankStation,
    "melter": MelterStation,
    "evaporator": EvaporatorStation,
    "pan": PanStation,
    "crystallizer": CrystallizerStation,
    "centrifugal": CentrifugalStation,
    "pump": PumpStation,
    "pressure_reducer": PressureReducerStation,
    "turbine": TurbineStation,
    "turbo_alternator": TurboAlternatorStation,
    "thermocompressor": ThermocompressorStation,
    "compressor": CompressorStation,
    "contact_condenser": ContactCondenserStation,
    "surface_condenser": SurfaceCondenserStation,
    "reactor": ReactorStation,
    "separator_filter": SeparatorFilterStation,
    "dryer": DryerStation,
}


def create_station(
    station_type: str,
    station_id: str,
    station_number: int,
    name: str,
    properties: Dict[str, Any],
) -> BaseStation:
    """Factory function instantiating the appropriate Station subclass."""
    st_clean = station_type.strip().lower()
    cls = STATION_REGISTRY.get(st_clean)
    if not cls:
        # Fallback to Receiver (standard mixing manifold) with a warning
        cls = ReceiverStation
    return cls(
        station_id=station_id,
        station_number=station_number,
        name=name,
        station_type=st_clean,
        properties=properties,
    )
