from rdflib import URIRef

from bob.connections.light import (
    LightInletConnectionPoint,
    LightInletZoneConnectionPoint,
    LightVisibleInletConnectionPoint,
    LightVisibleInletZoneConnectionPoint,
)
from bob.properties.states import OccupancyStatus

from ..core import Domain, DomainSpace, Light, Zone, BOB, P223, S223

_namespace = BOB


class LightingSpace(DomainSpace):
    _class_iri = P223.LightingSpace
    hasDomain = Domain.Lighting
    hasMedium = Light.Visible
    lightInlet: LightVisibleInletConnectionPoint
    naturalLightInlet: LightVisibleInletConnectionPoint
    occupancy: OccupancyStatus


class LightingZone(Zone):
    _class_iri = P223.LightingZone
    hasDomain = Domain.Lighting
    lightInlet: LightVisibleInletZoneConnectionPoint
    occupancy: OccupancyStatus
