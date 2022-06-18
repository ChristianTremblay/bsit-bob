from rdflib import URIRef

from bob.connections.light import (
    LightInletConnectionPoint,
    LightInletZoneConnectionPoint,
    LightVisibleInletConnectionPoint,
    LightVisibleInletZoneConnectionPoint,
)
from bob.properties.states import OccupancyStatus

from ..core import Domain, DomainSpace, Light, Zone, bob, p223, s223

_namespace = bob


class LightingSpace(DomainSpace):
    _class_iri = s223.LightingSpace
    hasDomain = Domain.Lighting
    hasMedium = Light.Visible
    lightInlet: LightVisibleInletConnectionPoint
    naturalLightInlet: LightVisibleInletConnectionPoint
    occupancy: OccupancyStatus


class LightingZone(Zone):
    _class_iri = s223.LightingZone
    hasDomain = Domain.Lighting
    lightInlet: LightVisibleInletZoneConnectionPoint
    occupancy: OccupancyStatus
