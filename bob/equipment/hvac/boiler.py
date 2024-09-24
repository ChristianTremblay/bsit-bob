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
from ...properties.temperature import Temperature
from ...template import template_update
from .coil import HeatpumpCoil, ImmersedResistanceHeaterElement
from .compressor import RefrigeartionGasCompressor
from .fan import Fan
from .filter import Filter
from .tank import Tank
from .valve import ExpansionValve, ReversingValve

_namespace = BOB


class HotWaterBoiler(Equipment):
    _class_iri = S223.Boiler
    hotWaterLeaving: HotWaterOutletConnectionPoint
    hotWaterEntering: HotWaterInletConnectionPoint


class ElectricalHotWaterBoiler(HotWaterBoiler):
    _class_iri = S223.Boiler
    electricalInlet: ElectricalInletConnectionPoint


class NaturalGasHotWaterBoiler(HotWaterBoiler):
    _class_iri = S223.Boiler
    electricalInlet: ElectricalInletConnectionPoint
    naturalGasInlet: NaturalGasInletConnectionPoint
    combustionAirInlet: AirInletConnectionPoint
    combustionAirOutlet: AirOutletConnectionPoint
    condensedWaterOutlet: WaterOutletConnectionPoint


domesticwaterheater_template = {
    "cp": {"electricalInlet": Electricity_240VLL_1Ph_60HzInletConnectionPoint},
    "properties": {
        ("leavingFluidTemperature", Temperature): {},
        ("enteringFluidTemperature", Temperature): {},
        ("fluidFlow", Flow): {"hasUnit": UNIT["L-PER-SEC"]},
    },
    "equipment": {
        ("tank", Tank): {
            "config": {"properties": {("fluidTemperature", Temperature): {}}},
            "hasRole": Role.Storage,
            "comment": "Water tank",
        },
        ("element1", ImmersedResistanceHeaterElement): {
            "comment": "Electrical element 1",
            "electricalInlet": Electricity_240VLL_1Ph_60HzInletConnectionPoint,
            "hasRole": Role.Heating,
        },
        ("element2", ImmersedResistanceHeaterElement): {
            "comment": "Electrical element 2",
            "electricalInlet": Electricity_240VLL_1Ph_60HzInletConnectionPoint,
            "hasRole": Role.Heating,
        },
    },
}


class DomesticElectricalWaterHeater(Equipment):
    _class_iri = P223.DomesticWaterHeater
    leavingFluid: WaterOutletConnectionPoint
    enteringFluid: WaterInletConnectionPoint

    fluidTemperature: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(domesticwaterheater_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self["tank"].set_medium(DomesticWater)
        self.leavingFluid.hasMedium = DomesticHotWater
        self.enteringFluid.hasMedium = DomesticWater
        self.heatExchangeConnection = WaterConnection(label="heatExchangeConnection")
        self["tank"].containedFluid >> self.heatExchangeConnection
        self["element1"].fluidContact >> self.heatExchangeConnection
        self["element2"].fluidContact >> self.heatExchangeConnection
        self["tank"].enteringFluid.mapsTo = self.enteringFluid
        self["tank"].leavingFluid.mapsTo = self.leavingFluid
        self.fluidTemperature = self["tank"]["fluidTemperature"]
        self["tank"].hasRole = Role.Storage
