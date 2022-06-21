from typing import Dict

from bob.properties.states import OnOffCommand, OnOffStatus

from ...connections.electricity import *
from ...core import Device, Node, BOB, P223, S223
from ...sensor.electricity import CurrentBinarySensor

_namespace = BOB


class MotorStarter(Device):
    """
    Motor starter
    This device provides command and status for an electrical
    device like a fan or a pump

    """

    _class_iri = P223.MotorStarter
    outputSignal: OnOffSignalOutletConnectionPoint
    inputSignal: OnOffSignalInletConnectionPoint
    onOffStatus: OnOffStatus
    onOffCommand: OnOffCommand

    def __init__(self, config: Dict = {}, **kwargs):
        # _config = template_update(starter_template, config)
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

        sensor = CurrentBinarySensor(
            label=f"{self.label}.sensor",
            ofMedium=self.electricalInlet.hasMedium,
            hasMeasurementLocation=self.electricalOutlet,
        )
        self.onOffStatus = sensor.observesProperty
        self._sensors = [sensor]
        self > sensor
