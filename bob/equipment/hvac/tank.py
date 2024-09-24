from typing import Any, Dict

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
from ...core import BOB, P223, S223, UNIT, Equipment, PropertyReference
from ...enum import DomesticHotWater, DomesticWater, Fluid, Role, Water
from ...properties.flow import Flow
from ...properties.force import Pressure
from ...properties.temperature import Temperature
from ...template import template_update
from .coil import HeatpumpCoil, ImmersedResistanceHeaterElement
from .compressor import RefrigeartionGasCompressor
from .fan import Fan
from .filter import Filter
from .valve import ExpansionValve, ReversingValve

_namespace = BOB


class Tank(Equipment):
    _class_iri = P223.Tank
    leavingFluid: FluidOutletConnectionPoint
    enteringFluid: FluidInletConnectionPoint
    containedFluid: FluidBidirectionalConnectionPoint

    fluidTemperature: Temperature
    internalPressure: Pressure

    # leavingFluidTemperature: Temperature
    # enteringFluidTemperature: Temperature
    # fluidFlow: Flow
    def set_medium(self, medium: Fluid = Water):
        self.containedFluid.hasMedium = medium
        self.enteringFluid.hasMedium = medium
        self.leavingFluid.hasMedium = medium
