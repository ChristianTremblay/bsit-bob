from rdflib import URIRef
from typing import Dict

from bob.property import QuantifiableObservableProperty
from ...connections.electricity import ElectricalInletConnectionPoint
from ...core import ConnectionPoint, s223, Device, quantitykind, unit


from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...signal import AnalogIn, AnalogOut
from ...sensor import define_sensors
from ...devices import contains_devices_list
from ...properties.electricity import Amps, ElectricPowerkW, PowerFactor
from ...properties.force import HP
from ...properties.ratio import RPM

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


class Fan(Device):
    node_type: URIRef = s223.Fan
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    # electricalInlet: ElectricalInletConnectionPoint  # Dynamic ConnectionPoint should not be defined in annotation of the class
    # Properties
    amps: Amps
    rpm: RPM
    hp: HP
    kW: ElectricPowerkW
    powerFactor: PowerFactor

    def __init__(self, config: Dict = None, **kwargs):
        optional_properties = ["amps", "rpm", "hp", "kW", "powerFactor"]
        _properties = {}
        if not config and not kwargs:
            raise ValueError(
                "Please provide configuration dict or kwargs, at least a label"
            )

        sensors = define_sensors(config)
        devices, device_kwargs = contains_devices_list(config, **kwargs)

        _electricalInlet = (
            device_kwargs.pop("electricalInlet")
            if "electricalInlet" in device_kwargs
            else None
        )

        for each in optional_properties:
            _properties[each] = (
                device_kwargs.pop(each) if each in device_kwargs else None
            )

        super().__init__(**device_kwargs)
        self.electricalInlet = (
            _electricalInlet(self, label=f"{self.label}.electricalInlet")
            if _electricalInlet
            else None
        )
        for k, v in _properties.items():
            if v:
                setattr(self, k, self.__annotations__[k](v))
        for sensor in sensors:
            self > sensor
        for dev in devices:
            self > dev
