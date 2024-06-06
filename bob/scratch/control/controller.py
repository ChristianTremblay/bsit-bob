from typing import Dict

from ...equipment.control.controller import Controller


from ...connections.electricity import ElectricalInletConnectionPoint
from ...connections.network import RS485BidirectionalConnectionPoint
from ...connections.mechanical import MechanicalOutletConnectionPoint
from ...scratch.hvac.actuator import ElectricalProportionalActuator

from ...core import SCRATCH, S223
from ...template import template_update
from ...properties import Nm, Percent, PercentCommand
from ...properties.states import OnOffCommand, OnOffStatus
from ...sensor.motion import PositionSensor

class _VAVController(Controller):
    """
    First make it a controller
    """

    _class_iri = S223.Controller


vav_controller_template = {
    "properties": {
        ("command", PercentCommand): {},
        ("position_feedback", Percent): {},
        ("is_open", OnOffStatus): {},
        ("is_closed", OnOffStatus): {},
        ("torque", Nm): {},
    }
}
class VAVController(ElectricalProportionalActuator):

    _class_iri = SCRATCH.VAVController
    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(vav_controller_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
