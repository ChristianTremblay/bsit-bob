from rdflib import URIRef

from bob.connections.air import (
    AirInletConnectionPoint,
    AirInletZoneConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletZoneConnectionPoint,
)
from ..core import DomainSpace, HVAC, s223, Zone

__namespace__ = s223


class HVACSpace(DomainSpace):
    hasDomain = HVAC
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint


class HVACZone(Zone):
    hasDomain = HVAC
    airInlet: AirInletZoneConnectionPoint
    airOutlet: AirOutletZoneConnectionPoint
