from rdflib import URIRef

from ..core import Domain, DomainSpace, PropertyReference, Light, Zone, BOB, P223, S223

from bob.connections.light import (
    LightInletConnectionPoint,
    LightInletZoneConnectionPoint,
    LightVisibleInletConnectionPoint,
    LightVisibleInletZoneConnectionPoint,
)
from bob.properties.states import OccupancyStatus


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
    # lightInlet: LightVisibleInletZoneConnectionPoint
    occupancy: PropertyReference  # promoted from a space
