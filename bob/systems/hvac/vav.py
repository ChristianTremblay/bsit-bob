from attr import set_run_validators
from rdflib import URIRef
from typing import Any, Dict
from ...connections.electricity import Electricity_575V_60HzSystemInletConnectionPoint
from ...core import p223, Device, System


from ...connections.air import (
    AirOutletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from ...signal import AnalogIn, AnalogOut
from ...sensor import define_sensors
from ...devices import contains_devices_list

__namespace__ = p223

vav_template = {
    "params": {"label": "Name", "comment": "Description"},
    "sensors": {},
    "contains": {("sub_device1_label", Device): {"comment": "SubDev comment"}},
}


class VAV(System):
    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint

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
        self._contains = devices
        self._contains.extend(sensors)

    def __getitem__(self, name: str) -> Any:
        for each in self._contains:
            if each.label == name:
                return each
