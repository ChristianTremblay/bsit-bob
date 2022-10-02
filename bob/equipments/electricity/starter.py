from typing import Dict
from bob.equipments.electricity import _MotorStarter
from bob.enum import HandOffAutoEnum
from bob.properties.electricity import ElectricPower
from bob.properties.ratio import Percent, PercentCommand

from bob.properties.states import OnOffCommand, OnOffStatus

from ...connections.electricity import *
from ...core import (
    Device,
    logging,
    Node,
    BOB,
    P223,
    S223,
    Property,
    UNIT,
    PropertyReference,
    template_update,
)
from ...sensor.electricity import CurrentBinarySensor

_namespace = BOB

electric_starter_template = {
    "cp": {
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
        "electricalOutlet": Electricity_575V_60HzOutletConnectionPoint,
    },
    "properties": {
        # ("actuatesProperty", PercentCommand): {},
        ("onOffCommand", OnOffCommand): {},
        ("power_rating", ElectricPower): {"unit": UNIT["HP_Electric"]},
    },
}


class MotorStarter(_MotorStarter):
    """
    Motor starter
    This device provides command and status for an electrical
    device like a fan or a pump

    """

    _class_iri = P223.MotorStarter
    outputSignal: OnOffSignalOutletConnectionPoint
    inputSignal: OnOffSignalInletConnectionPoint
    onOffStatus: PropertyReference
    onOffCommand: OnOffCommand  # this property could have `hasAspect` HandOffAutoEnum

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(electric_starter_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        logging.debug(f"MotorStarter.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)

        sensor = CurrentBinarySensor(
            label=f"{self.label}.current_sensor",
            ofMedium=self.electricalInlet.hasMedium,
            hasMeasurementLocation=self.electricalOutlet,
        )
        self.onOffStatus = sensor.observesProperty
        self._sensors = [sensor]
        self > sensor
