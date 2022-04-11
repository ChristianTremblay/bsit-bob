from rdflib import URIRef

from bob.connections.occupancy import (
    OccupancyInletConnectionPoint,
    OccupancyInletZoneConnectionPoint,
)

from ..core import DomainSpace, Medium, Occupancy, People, Zone, p223, s223
from ..systems.physic import IndoorAir

__namespace__ = p223


class OccupancySpace(DomainSpace):
    hasDomain = Occupancy
    hasMedium: Medium = People
    occupancyInlet: OccupancyInletConnectionPoint
    indoorAir: IndoorAir


class OccupancyZone(Zone):
    hasDomain = Occupancy
    occupancyInlet: OccupancyInletZoneConnectionPoint
