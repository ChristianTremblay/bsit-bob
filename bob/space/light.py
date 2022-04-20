from rdflib import URIRef

from bob.connections.light import (
    LightInletConnectionPoint,
    LightInletZoneConnectionPoint,
    LightVisibleInletConnectionPoint,
    LightVisibleInletZoneConnectionPoint,
)
from bob.connections.occupancy import (
    OccupancyInletConnectionPoint,
    OccupancyInletZoneConnectionPoint,
)
from bob.properties.states import OccupancyStatus

from ..core import DomainSpace, Light, Lighting, Medium, Zone, p223, s223
from ..systems.physic import IndoorAir

_namespace = p223


class LightingSpace(DomainSpace):
    hasDomain = Lighting
    hasMedium: Medium = Light
    lightInlet: LightVisibleInletConnectionPoint
    naturalLightInlet: LightVisibleInletConnectionPoint
    occupancy: OccupancyStatus


class LightingZone(Zone):
    hasDomain = Lighting
    lightInlet: LightVisibleInletZoneConnectionPoint
    occupancy: OccupancyStatus
