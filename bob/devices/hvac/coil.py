from typing import Any, Dict

from rdflib import URIRef

from bob.properties.electricity import Amps, ElectricPowerkW

from ...connections.air import (
    AirBidirectionalConnectionPoint,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
    Electricity_240V_60HzInletConnectionPoint,
    Electricity_575V_60HzInletConnectionPoint,
)
from ...connections.water import (
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...core import Device, PropertyReference, bob, p223, s223

_namespace = bob

coil_template = {
    "cp": {},
    "properties": {},
}


class Coil(Device):
    _class_iri = s223.Coil
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
    _class_iri = s223.Coil
    waterInlet: WaterInletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint

    def __init__(self, config: Dict = coil_template, **kwargs):
        config["properties"] = config.get("properties", coil_template["properties"])
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class ChilledWaterCoil(Coil):
    _class_iri = s223.CoolingCoil
    chilledWaterInlet: ChilledWaterInletConnectionPoint
    chilledWaterOutlet: ChilledWaterOutletConnectionPoint

    def __init__(self, config: Dict = coil_template, **kwargs):
        config["properties"] = config.get("properties", coil_template["properties"])
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class HotWaterCoil(Coil):
    _class_iri = s223.HeatingCoil
    hotWaterInlet: HotWaterInletConnectionPoint
    hotWaterOutlet: HotWaterOutletConnectionPoint

    def __init__(self, config: Dict = coil_template, **kwargs):
        config["properties"] = config.get("properties", coil_template["properties"])
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


# Electrical Coil
electricalheating_template = {
    "cp": {"electricalInlet": Electricity_575V_60HzInletConnectionPoint},
    "properties": {
        ("amps", Amps): {},
        ("kW", ElectricPowerkW): {},
    },
}


class ElectricalHeatingCoil(Coil):
    _class_iri = s223.HeatingCoil

    def __init__(self, config: Dict = electricalheating_template, **kwargs):
        config["properties"] = config.get(
            "properties", electricalheating_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


# Electrical Coil
electricalradiant_template = {
    "cp": {"electricalInlet": Electricity_240V_60HzInletConnectionPoint},
    "properties": {
        ("amps", Amps): {},
        ("kW", ElectricPowerkW): {},
    },
}

# Baseboard, radiant panel, heating floor
class ElectricalRadiantHeatingCoil(Device):
    _class_iri = s223.HeatingCoil
    airContact: AirBidirectionalConnectionPoint

    def __init__(self, config: Dict = electricalradiant_template, **kwargs):
        config["properties"] = config.get(
            "properties", electricalradiant_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
