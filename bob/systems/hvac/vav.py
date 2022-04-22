from typing import Any, Dict

from attr import set_run_validators
from rdflib import URIRef

from ...connections.air import (
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from ...connections.electricity import Electricity_575V_60HzSystemInletConnectionPoint
from ...core import Device, System, p223
from ...devices.hvac.damper import Damper
from ...signal import AnalogIn, AnalogOut

_namespace = p223

vav_template = {
    "params": {"label": "Name", "comment": "Description"},
    "sensors": {},
    "devices": {("sub_device1_label", Device): {"comment": "SubDev comment"}},
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

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class VAV1(System):
    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    airFlow: AnalogIn
    damperPosition: AnalogOut

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)

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
