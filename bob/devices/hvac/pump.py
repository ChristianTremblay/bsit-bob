from typing import Dict

from rdflib import URIRef

from ...connections.electricity import Electricity_575V_60HzInletConnectionPoint
from ...connections.water import WaterInletConnectionPoint, WaterOutletConnectionPoint
from ...core import Device, PropertyReference, BOB, S223, UNIT
from ...properties import (
    HP,
    RPM,
    Amps,
    ElectricPowerkW,
    OnOffStatus,
    PowerFactor,
    Pressure,
)

_namespace = BOB

pump_template = {
    "cp": {"electricalInlet": Electricity_575V_60HzInletConnectionPoint},
    "properties": {
        ("head_pressure", Pressure): {"unit": UNIT.PSI},
        ("amps", Amps): {},
        ("rpm", RPM): {},
        ("hp", HP): {},
        ("kW", ElectricPowerkW): {},
        ("powerFactor", PowerFactor): {},
    },
}


class Pump(Device):
    _class_iri = S223.Pump
    waterInlet: WaterInletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint
    onOffStatus: PropertyReference
    onOffCommand: PropertyReference

    def __init__(self, config: Dict = pump_template, **kwargs):
        config["properties"] = config.get("properties", pump_template["properties"])
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
