from typing import Any, Dict, List

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    Electricity_240VLL_1Ph_60HzInletConnectionPoint,
)
from ...connections.liquid import (
    FluidBidirectionalConnectionPoint,
    FluidInletConnectionPoint,
    FluidOutletConnectionPoint,
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    WaterBidirectionalConnectionPoint,
    WaterConnection,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...connections.naturalgas import NaturalGasInletConnectionPoint
from ...core import BOB, P223, S223, UNIT, ConnectionPoint, Equipment, PropertyReference
from ...enum import DomesticHotWater, DomesticWater, Fluid, Role, Water
from ...properties.flow import Flow
from ...properties.force import Pressure
from ...properties.temperature import Temperature
from ...template import template_update
from .coil import HeatpumpCoil, ImmersedResistanceHeaterElement
from .compressor import RefrigerationGasCompressor
from .fan import Fan
from .filter import Filter
from .valve import ExpansionValve, ReversingValve

_namespace = BOB


class Tank(Equipment):
    _class_iri = P223.Tank
    fluidInlet: FluidInletConnectionPoint
    fluidOutlet: FluidOutletConnectionPoint
    containedFluid: FluidBidirectionalConnectionPoint

    fluidTemperature: Temperature
    internalPressure: Pressure

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.fluidOutlet.paired_to(self.fluidInlet)

    def set_fluid_type(self, fluid: Fluid = Water):
        self.set_medium(["leavingFluid", "enteringFluid", "containedFluid"], fluid)
