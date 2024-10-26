import logging
from typing import Dict

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import BOB, S223, BoundaryConnectionPoint, Equipment, System
from ...equipment.hvac.damper import Damper
from ...sensor.flow import AirFlowSensor
from ...template import configure_relations, template_update

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB

TerminalUnit_template = {
    "equipment": {
        ("damper", Damper): {"comment": "VAV Box Damper including"},
        # ("flow_sensor", AirFlowSensor): {"comment": "Air flow sensor"}
    },
}


class SingleDuctTerminal(System):
    _class_iri = S223.SingleDuctTerminal
    airInlet: BoundaryConnectionPoint
    airOutlet: BoundaryConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(TerminalUnit_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.info(f"SingleDuctTerminal.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)
        self.airInlet = self["damper"].airInlet
        self.airOutlet = self["damper"].airOutlet
        # self['flow_sensor'] % self['damper'].airInlet
