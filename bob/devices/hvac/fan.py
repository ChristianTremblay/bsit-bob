import logging
from typing import Dict

from rdflib import URIRef

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...connections.electricity import Electricity_575V_60HzInletConnectionPoint
from ...core import (
    ConnectionPoint,
    Device,
    PropertyReference,
    bob,
    quantitykind,
    s223,
    unit,
)
from ...properties import HP, RPM, Amps, ElectricPowerkW, PowerFactor, Pressure
from ...properties.states import OnOffCommand, OnOffStatus
from ...property import QuantifiableObservableProperty

_namespace = bob

fan_template = {
    "cp": {"electricalInlet": Electricity_575V_60HzInletConnectionPoint},
    "properties": {
        ("staticPressure", Pressure): {"unit": unit.PA},
        ("amps", Amps): {},
        ("rpm", RPM): {},
        ("hp", HP): {},
        ("kW", ElectricPowerkW): {},
        ("powerFactor", PowerFactor): {},
    },
}


class Fan(Device):
    """
    A fan is composed of a blower and an electrical motor
    """

    _class_iri: URIRef = s223.Fan
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    onOffStatus: PropertyReference
    onOffCommand: PropertyReference

    def __init__(self, config: Dict = fan_template, **kwargs):
        config["properties"] = config.get("properties", fan_template["properties"])
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
