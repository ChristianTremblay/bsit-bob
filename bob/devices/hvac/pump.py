from rdflib import URIRef
from typing import Dict

from ...properties.force import HP

from ...properties.ratio import RPM

from ...properties.electricity import Amps, ElectricPowerkW, PowerFactor
from ...connections.electricity import ElectricalInletConnectionPoint
from ...core import s223, Device


from ...connections.water import WaterInletConnectionPoint, WaterOutletConnectionPoint
from ...sensor import define_sensors
from ...devices import contains_devices_list

__namespace__ = s223

"""
fan_template = {
    "params": {"label": "Name", "comment": "Description"},
    "sensors": {},
    "contains": {("sub_device1_label", Device): {"comment": "SubDev comment"}},
}
"""


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
