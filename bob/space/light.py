from rdflib import URIRef

from bob.connections.light import (
    LightInletConnectionPoint,
    LightInletZoneConnectionPoint,
    LightVisibleInletConnectionPoint,
    LightVisibleInletZoneConnectionPoint,
)
from bob.properties.states import OccupancyStatus

from ..core import BOB, P223, S223, Domain, DomainSpace, Light, PropertyReference, Zone

_namespace = BOB


class LightingSpace(DomainSpace):
    _class_iri = BOB.LightingSpace
    hasDomain = Domain.Lighting
    hasMedium = Light.Visible
    lightInlet: LightVisibleInletConnectionPoint
    naturalLightInlet: LightVisibleInletConnectionPoint
    occupancy: OccupancyStatus


class LightingZone(Zone):
    _class_iri = BOB.LightingZone
    hasDomain = Domain.Lighting
    # lightInlet: LightVisibleInletZoneConnectionPoint
    occupancy: PropertyReference  # promoted from a space
