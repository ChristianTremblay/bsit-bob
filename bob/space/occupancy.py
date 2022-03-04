from rdflib import URIRef

from bob.connections.occupancy import (
    OccupancyInletConnectionPoint,
    OccupancyInletZoneConnectionPoint,
)
from ..core import DomainSpace, Occupancy, p223, Zone, s223, Medium, People
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
