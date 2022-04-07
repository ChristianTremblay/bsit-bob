import logging
from typing import Dict

from rdflib import URIRef

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...connections.electricity import ElectricalInletConnectionPoint
from ...core import ConnectionPoint, Device, PropertyReference, quantitykind, s223, unit
from ...properties import HP, RPM, Amps, ElectricPowerkW, PowerFactor, Pressure
from ...properties.states import OnOffCommand, OnOffStatus
from ...property import QuantifiableObservableProperty
from ...signal import AnalogIn, AnalogOut

__namespace__ = s223

"""
fan_template = {
    "params": {
        "label": "MyFan", 
        "comment": "A Big Fan",
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
        "amps": 10,
        "hp": 10,
        "rpm": 1770,
        "powerFactor": 1.4
    },
    "sensors": {},
    "devices": {},
}
"""


class Fan(Device):
    """
    A fan is composed of a blower and an electrical motor
    """

    node_type: URIRef = s223.Fan
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    # electricalInlet: ElectricalInletConnectionPoint  # Dynamic ConnectionPoint should not be defined in annotation of the class
    # Properties
    staticPressure: Pressure
    amps: Amps
    rpm: RPM
    hp: HP
    kW: ElectricPowerkW
    powerFactor: PowerFactor
    hasOnOffStatus: PropertyReference
    hasOnOffCommand: PropertyReference

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        _electricalInlet = kwargs.pop("electricalInlet", None)

        super().__init__(config, **kwargs)

        if _electricalInlet:
            self.electricalInlet = _electricalInlet(
                self, label=f"{self.label}.electricalInlet"
            )
