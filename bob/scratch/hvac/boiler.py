from typing import Dict

from bob import application
from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.connections.electricity import Electricity_240VLL_1Ph_60HzInletConnectionPoint
from bob.connections.liquid import (
    WaterBidirectionalConnectionPoint,
    WaterConnection,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from bob.core import (
    S223,
    SCRATCH,
    UNIT,
    BoundaryConnectionPoint,
    Equipment,
    PropertyReference,
)
from bob.enum import Role
from bob.equipment.hvac.coil import HeatpumpCoil, ImmersedResistanceHeaterElement
from bob.equipment.hvac.compressor import RefrigerationGasCompressor
from bob.equipment.hvac.fan import Fan
from bob.equipment.hvac.filter import Filter
from bob.equipment.hvac.tank import Tank
from bob.equipment.hvac.valve import ExpansionValve
from bob.functions import Function, FunctionInput, FunctionOutput
from bob.properties.flow import Flow
from bob.properties.temperature import Temperature
from bob.template import SystemFromTemplate, template_update

_namespace = SCRATCH

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


class InsideTankHeatTransfer(Function):
    """ """

    _class_iri = SCRATCH.InsideTankHeatTransfer

    waterFlow: FunctionInput
    averageSurfaceTemperature: FunctionInput
    resistanceHeaterPower1: FunctionInput
    resistanceHeaterModulation1: FunctionInput
    resistanceHeaterCommand1: FunctionInput
    resistanceHeaterPower2: FunctionInput
    resistanceHeaterModulation2: FunctionInput
    resistanceHeaterCommand2: FunctionInput
    leavingWaterTemp: FunctionOutput
    fluidTemp: FunctionOutput


class _DomesticElectricalWaterHeater(Equipment):
    _class_iri = SCRATCH.DomesticElectricalWaterHeater
    fluidOutlet: WaterOutletConnectionPoint
    fluidInlet: WaterInletConnectionPoint
    # electricalInlet: ElectricalInletConnectionPoint
    fluidTemperature: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(domesticwaterheater_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        # self["tank"].set_medium(DomesticWater)
        # self.leavingFluid.hasMedium = DomesticHotWater
        # self.enteringFluid.hasMedium = DomesticWater
        self.heatExchangeConnection = WaterConnection(label="heatExchangeConnection")
        self["tank"].containedFluid >> self.heatExchangeConnection
        self["element1"].fluidContact >> self.heatExchangeConnection
        self["element2"].fluidContact >> self.heatExchangeConnection
        self["tank"].fluidInlet.mapsTo = self.fluidInlet
        self["tank"].fluidOutlet.mapsTo = self.fluidOutlet
        self.fluidTemperature = self["tank"]["fluidTemperature"]
        self["tank"] += Role.Storage
        self += Role.Heating

        heat_transfer = InsideTankHeatTransfer(
            label="Heat Transfer Function",
            waterFlow=self["fluidFlow"],
            resistanceHeaterPower1=self["element1"]["kW"],
            resistanceHeaterModulation1=self["element1"]["modulation"],
            resistanceHeaterCommand1=self["element1"]["onOffCommand"],
            resistanceHeaterPower2=self["element2"]["kW"],
            resistanceHeaterModulation2=self["element2"]["modulation"],
            resistanceHeaterCommand2=self["element2"]["onOffCommand"],
            leavingWaterTemp=self["leavingFluidTemperature"],
            fluidTemp=self["tank"]["fluidTemperature"],
        )


scratch_system_template = {
    "params": {"label": "HotWaterHeater", "comment": "Hot Water Heater"},
    "equipment": {
        ("DomesticHotWaterHeater", _DomesticElectricalWaterHeater): {},
    },
    "relations": [
        ("self.fluidOutlet", "=", "self['DomesticHotWaterHeater'].fluidOutlet"),
        ("self.fluidInlet", "=", "self['DomesticHotWaterHeater'].fluidInlet"),
        ("self.electricalInlet", "=", "self['DomesticHotWaterHeater'].electricalInlet"),
    ],
}


class DomesticHotWaterHeater(SystemFromTemplate, application.HotWaterHeater):
    _class_iri = SCRATCH.DomesticHotWaterHeater
    fluidOutlet: BoundaryConnectionPoint
    fluidInlet: BoundaryConnectionPoint
    electricalInlet: BoundaryConnectionPoint

    def __init__(self, config: Dict = scratch_system_template, **kwargs) -> None:
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self += Role.Heating


domesticHPwaterheater_template = {
    "cp": {"electricalInlet": Electricity_240VLL_1Ph_60HzInletConnectionPoint},
    "properties": {
        ("leavingFluidTemperature", Temperature): {},
        ("enteringFluidTemperature", Temperature): {},
        ("fluidFlow", Flow): {"hasUnit": UNIT["L-PER-SEC"]},
    },
    "equipment": {
        ("TANK", Tank): {
            "config": {"properties": {("fluidTemperature", Temperature): {}}},
            "hasRole": Role.Storage,
            "comment": "Water tank",
        },
        ("ELEMENT1", ImmersedResistanceHeaterElement): {
            "comment": "Electrical element 1",
            "electricalInlet": Electricity_240VLL_1Ph_60HzInletConnectionPoint,
            "hasRole": Role.Heating,
        },
        ("ELEMENT2", ImmersedResistanceHeaterElement): {
            "comment": "Electrical element 2",
            "electricalInlet": Electricity_240VLL_1Ph_60HzInletConnectionPoint,
            "hasRole": Role.Heating,
        },
        ("EVAPORATORFAN", Fan): {
            "comment": "Evaporator Fan",
            "electricalInlet": Electricity_240VLL_1Ph_60HzInletConnectionPoint,
        },
        ("CONDENSERCOIL", HeatpumpCoil): {
            "comment": "Condenser Coil",
            "config": {"cp": {"fluidContact": WaterBidirectionalConnectionPoint}},
        },
        ("EVAPORATORCOIL", HeatpumpCoil): {"comment": "Evaporator coil"},
        ("COMPRESSOR", RefrigerationGasCompressor): {"comment": "Compressor"},
        ("EXPANSIONVALVE", ExpansionValve): {"comment": "Expansion Valve"},
        ("FILTER", Filter): {"comment": "Filter"},
    },
}


class _DomesticHPWaterHeater(
    Equipment, application.HotWaterHeater, application.HeatPump
):
    _class_iri = SCRATCH.DomesticHeatPumpWaterHeater
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    fluidOutlet: WaterOutletConnectionPoint
    fluidInlet: WaterInletConnectionPoint

    def __init__(self, config: Dict = domesticHPwaterheater_template, **kwargs):
        _config = template_update({}, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.heatExchangeConnection = WaterConnection(label="heatExchangeConnection")
        self["EVAPORATORCOIL"] += Role.Evaporator
        self["CONDENSERCOIL"] += Role.Condenser
        self["CONDENSERCOIL"] += Role.Heating
        self["COMPRESSOR"].dischargePort >> self["CONDENSERCOIL"].gasPortA
        self["CONDENSERCOIL"].gasPortB >> self["EXPANSIONVALVE"].portA
        self["CONDENSERCOIL"].fluidContact >> self.heatExchangeConnection
        self["EXPANSIONVALVE"].portB >> self["EVAPORATORCOIL"].gasPortA
        self["EVAPORATORCOIL"].gasPortB >> self["COMPRESSOR"].returnPort

        # takes air from outside of water heater
        # ambiant -> self['FILTER'].airInlet
        self["FILTER"].airOutlet >> self["EVAPORATORCOIL"].airInlet
        self["EVAPORATORCOIL"].airOutlet >> self["EVAPORATORFAN"].airInlet
        # self['EVAPORATORFAN'].airOutlet -> ambiant
        # push air to outdoor

        self["FILTER"].airInlet.mapsTo = self.airInlet
        self["EVAPORATORFAN"].airOutlet.mapsTo = self.airOutlet

        # Relate the temperature of the surface of the condenser coil and the water flow in the tank to the temperature of the water leaving the tank
        heat_transfer = InsideTankHeatTransfer(
            label="Heat Transfer Function",
            averageSurfaceTemperature=self["CONDENSERCOIL"][
                "averageSurfaceTemperature"
            ],
            waterFlow=self["fluidFlow"],
            resistanceHeaterPower1=self["ELEMENT1"]["kW"],
            resistanceHeaterModulation1=self["ELEMENT1"]["modulation"],
            resistanceHeaterCommand1=self["ELEMENT1"]["onOffCommand"],
            resistanceHeaterPower2=self["ELEMENT2"]["kW"],
            resistanceHeaterModulation2=self["ELEMENT2"]["modulation"],
            resistanceHeaterCommand2=self["ELEMENT2"]["onOffCommand"],
            leavingWaterTemp=self["leavingFluidTemperature"],
            fluidTemp=self["TANK"]["fluidTemperature"],
        )

        self["TANK"].containedFluid >> self.heatExchangeConnection
        self["ELEMENT1"].fluidContact >> self.heatExchangeConnection
        self["ELEMENT2"].fluidContact >> self.heatExchangeConnection
        self["TANK"].fluidInlet.mapsTo = self.fluidInlet
        self["TANK"].fluidOutlet.mapsTo = self.fluidOutlet
        self.fluidTemperature = self["TANK"]["fluidTemperature"]
        self["TANK"] += Role.Storage
        self += Role.Heating


scratch_system_template = {
    "params": {"label": "HotWaterHeater", "comment": "Hot Water Heater"},
    "equipment": {
        ("DomesticHPWaterHeater", _DomesticHPWaterHeater): {},
    },
    "relations": [
        ("self.fluidOutlet", "=", "self['DomesticHPWaterHeater'].fluidOutlet"),
        ("self.fluidInlet", "=", "self['DomesticHPWaterHeater'].fluidInlet"),
        ("self.electricalInlet", "=", "self['DomesticHPWaterHeater'].electricalInlet"),
    ],
}


class DomesticHPWaterHeater(
    SystemFromTemplate, application.HotWaterHeater, application.HeatPump
):
    _class_iri = SCRATCH.DomesticHotWaterHeater
    fluidOutlet: BoundaryConnectionPoint
    fluidInlet: BoundaryConnectionPoint
    electricalInlet: BoundaryConnectionPoint

    def __init__(self, config: Dict = scratch_system_template, **kwargs) -> None:
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self += Role.Heating
