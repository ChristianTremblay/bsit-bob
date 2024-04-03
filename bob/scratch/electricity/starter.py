from typing import Dict

from bob.connections import electricity as elec_cnx
from bob.connections.controlsignal import (OnOffSignalInletConnectionPoint,
                                           OnOffSignalOutletConnectionPoint)
from bob.core import (BOB, P223, S223, SCRATCH, UNIT, Equipment, Node,
                      Property, PropertyReference, logging)
from bob.enum import HandOffAutoEnum
from bob.equipment.electricity.starter import MotorStarter as BasicMotorStarter
from bob.equipment.electricity.switch import CurrentRelay
from bob.properties.electricity import ElectricPower
from bob.properties.ratio import Percent, PercentCommand
from bob.properties.states import OnOffCommand, OnOffStatus
from bob.template import template_update, configure_relations

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = SCRATCH

electric_starter_template = {
    "cp": {
        "electricalInlet": elec_cnx.Electricity_600VLL_3Ph_60HzInletConnectionPoint,
        "electricalOutlet": elec_cnx.Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
    },
    "sensors": {
        ("currentRelay", CurrentRelay): {},
    },
    "properties": {
        # ("actuatesProperty", PercentCommand): {},
        ("onOffCommand", OnOffCommand): {},
        ("powerRating", ElectricPower): {"hasUnit": UNIT["HP_Electric"]},
    },
}


class MotorStarter_600VLL_3Ph_60Hz(BasicMotorStarter):
    """
    Motor starter
    This Equipment provides command and status for an electrical
    Equipment like a fan or a pump
    This prototype is a 600V 3phases motor starter that implements 
    onOffCommand and onOffStatus properties
    status is given by a current relay that is connected to the electrical outlet, that read
    current using its current sensor.

    """

    _class_iri = SCRATCH.MotorStarter_600VLL_3Ph_60Hz
    outputSignal: OnOffSignalOutletConnectionPoint
    inputSignal: OnOffSignalInletConnectionPoint
    onOffStatus: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(electric_starter_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"MotorStarter.__init__ {_config} {kwargs}")
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _config.pop("relations", []))

        if self["currentRelay"]:
            self.onOffStatus = self["currentRelay"]["onOffStatus"]
            self["currentRelay"]["currentSensor"] % self.electricalOutlet
