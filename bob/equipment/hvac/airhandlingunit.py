import logging
from typing import Dict


from ... import application
from ...core import BOB, BoundaryConnectionPoint, System, S223, Equipment
from ...template import SystemFromTemplate, template_update
from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint


# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB

class AirHandlingUnit(Equipment):
    _class_iri = S223.AirHandlingUnit
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint