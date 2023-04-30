from typing import Dict

from bob.enum import HandOffAutoEnum
from bob.equipment.electricity import _MotorStarter
from bob.properties.electricity import ElectricPower
from bob.properties.ratio import Percent, PercentCommand
from bob.properties.states import OnOffCommand, OnOffStatus

from ...connections.electricity import *
from ...core import (
    BOB,
    P223,
    S223,
    UNIT,
    Equipment,
    Node,
    Property,
    PropertyReference,
    logging,
    template_update,
)
from .switch import CurrentRelay

_namespace = BOB

electric_starter_template = {
    "cp": {
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
        "electricalOutlet": Electricity_575V_60HzOutletConnectionPoint,
    },
    "sensors": {
        ("currentRelay", CurrentRelay): {},
    },
    "properties": {
        # ("actuatesProperty", PercentCommand): {},
        ("onOffCommand", OnOffCommand): {},
        ("powerRating", ElectricPower): {"unit": UNIT["HP_Electric"]},
    },
}


class MotorStarter(_MotorStarter):
    """
    Motor starter
    This Equipment provides command and status for an electrical
    Equipment like a fan or a pump

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

        if self["currentRelay"]:
            self.onOffStatus = self["currentRelay"]["onOffStatus"]
            self["currentRelay"]["currentSensor"] % self.electricalOutlet
