from typing import Dict

from bob.devices.electricity.switch import CurrentSwitch
from bob.properties.states import OnOffCommand, OnOffStatus

from ...connections.electricity import *
from ...core import Device, Node, p223, s223
from ...sensor.electricity import CurrentBinarySensor

_namespace = s223


class MotorStarter(Device):
    """
    Motor starter
    This device provides command and status for an electrical
    device like a fan or a pump

    """

    node_type = s223.MotorStarter
    hasStatusOutlet: OnOffSignalOutletConnectionPoint
    hasCommandInlet: OnOffSignalInletConnectionPoint
    hasOnOffStatus: OnOffStatus
    hasOnOffCommand: OnOffCommand

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        _electricalInlet = kwargs.pop("electricalInlet")
        _electricalOutlet = kwargs.pop("electricalOutlet")

        super().__init__(config, **kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet"
        )

        sensor = CurrentSwitch(
            label=f"{self.label}.sensor",
            ofMedium=self.electricalInlet.hasMedium,
            hasMeasurementLocation=self.electricalOutlet,
        )
        self._sensors = [sensor]
        self > sensor
