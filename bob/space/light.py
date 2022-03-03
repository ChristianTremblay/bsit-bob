from rdflib import URIRef

from bob.connections.light import (
    LightInletConnectionPoint,
    LightInletZoneConnectionPoint,
)
from ..core import DomainSpace, Lighting, p223, Zone, s223, Medium, Light
from ..systems.physic import IndoorAir

__namespace__ = p223


class LightingSpace(DomainSpace):
    hasDomain = Lighting
    hasMedium: Medium = Light
    lightInlet: LightInletConnectionPoint
    naturalLightInlet: LightInletConnectionPoint
    indoorAir: IndoorAir


class LightingZone(Zone):
    hasDomain = Lighting
    lightInlet: LightInletZoneConnectionPoint
