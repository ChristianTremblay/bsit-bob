from typing import Any, Dict

from rdflib import URIRef

from bob.properties import Percent, PercentCommand
from bob.properties.electricity import Amps, ElectricPowerkW
from bob.properties.states import OnOffCommand, OnOffStatus

from ...connections.air import (
    AirBidirectionalConnectionPoint,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
    Electricity_240VLL_1Ph_60HzInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
)
from ...connections.liquid import (
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    WaterBidirectionalConnectionPoint,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...connections.refrigerant import (
    RefrigerantBidirectionalConnectionPoint,
    RefrigerantInletConnectionPoint,
    RefrigerantOutletConnectionPoint,
)
from ...core import BOB, P223, S223, Equipment, PropertyReference
from ...enum import (  # , R134a, R404a, R407c, R448a, R449a, R452a, R454b, R507a
    R22,
    R32,
    R410a,
    Refrigerant,
)
from ...properties.force import Pressure
from ...properties.temperature import Temperature
from ...template import template_update

_namespace = BOB

coil_template = {
    "cp": {},
    "properties": {
        ("averageSurfaceTemperature", Temperature): {},
        ("internalPressure", Pressure): {},
        ("internalTemperature", Temperature): {},
    },
}


class Coil(Equipment):
    _class_iri = S223.Coil
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    # Those could come from a valve, SCR, Triac, etc...
    modulation: PropertyReference
    onOffCommand: PropertyReference

    def __init__(self, config: Dict = coil_template, **kwargs):
        config["properties"] = config.get("properties", coil_template["properties"])
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class WaterCoil(Coil):
    _class_iri = S223.Coil
    waterInlet: WaterInletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint

    def __init__(self, config: Dict = coil_template, **kwargs):
        config["properties"] = config.get("properties", coil_template["properties"])
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class ChilledWaterCoil(Coil):
    _class_iri = S223.CoolingCoil
    chilledWaterInlet: ChilledWaterInletConnectionPoint
    chilledWaterOutlet: ChilledWaterOutletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


class HotWaterCoil(Coil):
    _class_iri = S223.HeatingCoil
    hotWaterInlet: HotWaterInletConnectionPoint
    hotWaterOutlet: HotWaterOutletConnectionPoint

    def __init__(self, config: Dict = coil_template, **kwargs):
        _config = template_update({}, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


class HeatpumpCoil(Coil):
    _class_iri = S223.Coil
    gasPortA: RefrigerantBidirectionalConnectionPoint
    gasPortB: RefrigerantBidirectionalConnectionPoint
    # airInlet: AirInletConnectionPoint
    # airOutlet: AirOutletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(coil_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)

    def set_gas_type(self, gas: Refrigerant):
        self.set_medium(["gasPortA", "gasPortB"], gas)


# Electrical Coil
electricalheating_template = {
    "cp": {"electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint},
    "properties": {
        ("amps", Amps): {},
        ("kW", ElectricPowerkW): {},
        ("modulation", PercentCommand): {},
        ("onOffCommand", OnOffCommand): {},
    },
}


class ElectricalHeatingCoil(Coil):
    _class_iri = S223.ElectricResistanceElement

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(electricalheating_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


# Electrical Coil
electricalradiant_template = {
    "cp": {"electricalInlet": Electricity_240VLL_1Ph_60HzInletConnectionPoint},
    "properties": {
        ("amps", Amps): {},
        ("kW", ElectricPowerkW): {},
    },
}


# Baseboard, radiant panel, heating floor
class ElectricalRadiantHeatingCoil(Equipment):
    _class_iri = S223.RadiantHeater
    airContact: AirBidirectionalConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(electricalradiant_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


# Water heaters
element_template = {
    "cp": {"electricalInlet": Electricity_240VLL_1Ph_60HzInletConnectionPoint},
    "properties": {
        ("amps", Amps): {},
        ("kW", ElectricPowerkW): {},
        ("modulation", PercentCommand): {},
        ("onOffCommand", OnOffCommand): {},
    },
}


class ImmersedResistanceHeaterElement(Equipment):
    _class_iri = S223.ElectricResistanceElement
    fluidContact: WaterBidirectionalConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(element_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
