from rdflib import URIRef
from typing import Dict
from ...connections.electricity import ElectricalInletConnectionPoint
from ...core import s223, Device


from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...signal import AnalogIn, AnalogOut
from ...sensor import define_sensors
from ...devices import contains_devices_list

__namespace__ = s223

fan_template = {
    "device": {"label": "Name", "comment": "Description"},
    "sensors": {},
    "contains": {("sub_device1_label", Device): {"comment": "SubDev comment"}},
}


class Fan(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    electricalInlet: ElectricalInletConnectionPoint  # can come from a VFD

    def __init__(self, config: Dict = None, **kwargs):
        if not config and not kwargs:
            raise ValueError(
                "Please provide configuration dict or kwargs, at least a label"
            )

        sensors = define_sensors(config)
        devices, device_kwargs = contains_devices_list(config, **kwargs)

        super().__init__(**device_kwargs)
        for sensor in sensors:
            self > sensor
        for dev in devices:
            self > dev
