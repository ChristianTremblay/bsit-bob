from rdflib import URIRef

from bob.connections.light import (
    LightInletConnectionPoint,
    LightInletZoneConnectionPoint,
    LightVisibleInletConnectionPoint,
    LightVisibleInletZoneConnectionPoint,
)
from bob.properties.states import OccupancyStatus

from ..core import Domain, DomainSpace, Light, Zone, p223, s223

_namespace = p223


class LightingSpace(DomainSpace):
    hasDomain = Domain.Lighting
    hasMedium = Light.Visible
    lightInlet: LightVisibleInletConnectionPoint
    naturalLightInlet: LightVisibleInletConnectionPoint
    occupancy: OccupancyStatus


class LightingZone(Zone):
    hasDomain = Domain.Lighting
    lightInlet: LightVisibleInletZoneConnectionPoint
    occupancy: OccupancyStatus
