from rdflib import URIRef

from bob.connections.light import (
    LightInletConnectionPoint,
    LightInletZoneConnectionPoint,
)
from ..core import DomainSpace, Lighting, p223, Zone, s223
from ..systems.physic import IndoorAir

__namespace__ = p223


class LightingSpace(DomainSpace):
    hasDomain = Lighting
    hasMedium = s223["Medium-Light"]
    lightInlet: LightInletConnectionPoint
    indoorAir: IndoorAir


class LightingZone(Zone):
    hasDomain = Lighting
    lightInlet: LightInletZoneConnectionPoint
