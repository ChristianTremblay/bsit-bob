from attr import set_run_validators
from rdflib import URIRef
from typing import Any, Dict
from ...connections.electricity import Electricity_575V_60HzSystemInletConnectionPoint
from ...core import p223, Device, System


from ...connections.air import (
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from ...signal import AnalogIn, AnalogOut
from ...sensor import define_sensors
from ...devices import contains_devices_list
from ...devices.hvac.damper import Damper

__namespace__ = p223

vav_template = {
    "params": {"label": "Name", "comment": "Description"},
    "sensors": {},
    "contains": {("sub_device1_label", Device): {"comment": "SubDev comment"}},
}


class AirFlowStation(Device):
    """
    This air flow station is designed to have air pass through the thing as a
    device so it has air inlets and outlets.  Contained in the device should
    be an AirFlowSensor.
    """
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    flow = AnalogIn


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


class VAV1(System):
    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    airFlow: AnalogIn
    damperPosition: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create an air flow station
        self.air_flow_station = AirFlowStation(label=self.label + ".air_flow_station")
        self > self.air_flow_station

        # create a damper
        self.damper = Damper(label=self.label + ".damper")
        self > self.damper

        # link the air pieces together
        self.air_flow_station >> self.damper

        # reference the connections
        self.airInlet.mapsTo = self.air_flow_station.airInlet
        self.airOutlet.mapsTo = self.damper.airOutlet
        self.airFlow = self.air_flow_station.flow
        self.damperPosition = self.damper.position
