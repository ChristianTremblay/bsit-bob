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
from ...core import (
    BOB,
    P223,
    S223,
    UNIT,
    BoundaryConnectionPoint,
    Equipment,
    PropertyReference,
    System,
)
from ...enum import DomesticHotWater, DomesticWater, Fluid, Role, Water
from ...properties.flow import Flow
from ...properties.temperature import Temperature
from ...template import SystemFromTemplate, template_update
from .coil import HeatpumpCoil, ImmersedResistanceHeaterElement
from .compressor import RefrigerationGasCompressor
from .fan import Fan
from .filter import Filter
from .tank import Tank
from .valve import ExpansionValve, ReversingValve

_namespace = BOB

# if no configuration is passed, use this basic template of a generic hot water heater equipment
basic_hotwaterheater_template = {
    "params": {"label": "HotWaterHeater", "comment": "Hot Water Heater"},
    "equipment": {
        ("hw_heater", Equipment): {
            "config": {
                "cp": {
                    "hotWaterLeaving": HotWaterOutletConnectionPoint,
                    "hotWaterEntering": HotWaterInletConnectionPoint,
                    "electricalInlet": ElectricalInletConnectionPoint,
                }
            },
        },
    },
    "relations": [
        ("self.leavingFluid", "=", "self['hw_heater'].hotWaterLeaving"),
        ("self.enteringFluid", "=", "self['hw_heater'].hotWaterEntering"),
        ("self.electricalInlet", "=", "self['hw_heater'].electricalInlet"),
    ],
}


# 223 Standard Systems
class DomesticHotWaterHeater(SystemFromTemplate):
    _class_iri = S223.DomesticHotWaterHeater
    leavingFluid: BoundaryConnectionPoint
    enteringFluid: BoundaryConnectionPoint
    electricalInlet: BoundaryConnectionPoint

    def __init__(self, config: Dict = basic_hotwaterheater_template, **kwargs) -> None:
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self += Role.Heating


# 223 Standard Equipment
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
