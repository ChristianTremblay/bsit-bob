from rdflib import URIRef
from typing import Dict

from ...properties import Amps, ElectricPowerkW, PowerFactor, RPM, HP, OnOffStatus
from ...connections.electricity import ElectricalInletConnectionPoint
from ...core import PropertyReference, s223, Device


from ...connections.water import WaterInletConnectionPoint, WaterOutletConnectionPoint
from ...sensor import define_sensors
from ...devices import composite, contains_devices_list

__namespace__ = s223

"""
fan_template = {
    "params": {"label": "Name", "comment": "Description"},
    "sensors": {},
    "contains": {("sub_device1_label", Device): {"comment": "SubDev comment"}},
}
"""


@composite
class Pump(Device):
    node_type: URIRef = s223.Fan
    waterInlet: WaterInletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint
    # electricalInlet: ElectricalInletConnectionPoint  # can come from a VFD
    # Properties
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
