from bob.devices.electricity.switch import CurrentSwitch
from bob.properties.states import OnOffCommand, OnOffStatus
from ...connections.electricity import *
from ...sensor.electricity import CurrentBinarySensor, create_3phases_meter_sensors

from ...core import Device, Node, s223, p223

from typing import Any

__namespace__ = s223


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

    def __init__(self, **kwargs):
        _electricalInlet = kwargs.pop("electricalInlet", None)
        _electricalOutlet = kwargs.pop("electricalOutlet", None)
        if not _electricalInlet or not _electricalOutlet:
            raise ValueError("Provide electricalInlet and electricalOutlet")

        super().__init__(**kwargs)
        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet"
        )

        self.sensor = CurrentSwitch(
            label=f"{self.label}.sensor",
            measuresMedium=self.electricalInlet.hasMedium,
            hasMeasurementLocation=self.electricalOutlet,
        )

    def finalize(self):
        self.sensor.finalize()
        self > self.sensor
        return self
