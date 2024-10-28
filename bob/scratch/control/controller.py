import logging
from typing import Dict

from ...equipment.control.controller import Controller


from ...core import SCRATCH, S223
from ...template import template_update
from ...properties import Percent, PercentCommand
from ...template import configure_relations

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = SCRATCH

vav_controller_template = {
    "properties": {
        ("damper_command", PercentCommand): {},
        ("damper_position_feedback", Percent): {},
    },
}


class VAVController(Controller):
    """
    A VAV Controller contains an actuator and a position sensor.
    It is meant to be used in a VAV (Terminal Unit) configuration.

    """

    _class_iri = S223.Controller

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(vav_controller_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
