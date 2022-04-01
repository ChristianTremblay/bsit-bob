from rdflib import URIRef
from typing import Dict
from ...properties.states import OnOffCommand, OnOffStatus

from ...property import QuantifiableObservableProperty
from ...connections.electricity import ElectricalInletConnectionPoint
from ...core import ConnectionPoint, PropertyReference, s223, Device, quantitykind, unit


from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...signal import AnalogIn, AnalogOut
from ...sensor import define_sensors
from ...devices import composite, contains_devices_list
from ...properties import Amps, ElectricPowerkW, PowerFactor, HP, Pressure, RPM

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
    "contains": {},
}
"""


@composite
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

    def __init__(self, config: Dict = None, **kwargs):
        _properties = {}
        for k, v in self.__annotations__.items():
            if k in kwargs:
                _properties[k] = kwargs.pop(k)
        if not config and not kwargs:
            raise ValueError(
                "Please provide configuration dict or kwargs, at least a label"
            )

        sensors = define_sensors(config)
        devices, device_kwargs = contains_devices_list(config, **kwargs)

        _electricalInlet = device_kwargs.pop("electricalInlet", None)

        super().__init__(**device_kwargs)
        self.electricalInlet = (
            _electricalInlet(self, label=f"{self.label}.electricalInlet")
            if _electricalInlet
            else None
        )
        for k, v in _properties.items():
            if v is not None:
                setattr(self, k, self.__annotations__[k](v))
        self.compose(sensors, devices)
