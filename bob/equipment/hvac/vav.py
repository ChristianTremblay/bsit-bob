import logging
from typing import Dict


from ...connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)
from ...core import BOB, S223, Equipment
from ...equipment.hvac.damper import Damper
from ...template import template_update, configure_relations

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB

TerminalUnit_template = {
    "equipment": {
        ("damper", Damper): {
            "comment": "VAV Box Damper including"
        }
    },
}

class VAV(Equipment):
    _class_iri = S223.SingleDuctTerminal
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    #damper: Damper provided via template

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(TerminalUnit_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.info(f"VAV.__init__ {_config} {kwargs}")
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
        self["damper"].airInlet.mapsTo = self.airInlet
        self["damper"].airOutlet.mapsTo = self.airOutlet

