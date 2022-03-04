from rdflib import URIRef

from ..core import (
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    BidirectionalConnectionPoint,
    Medium,
    SystemConnectionPoint,
    ZoneConnectionPoint,
    InletZoneConnectionPoint,
    OutletZoneConnectionPoint,
    BidirectionalSystemConnectionPoint,
)
from ..core import s223, enum
from ..signal import AnalogIn, AnalogOut

__namespace__ = s223

# === Occupancy
class Occupancy(Medium):
    node_type: URIRef = s223["Medium-Occupancy"]
    label = "Medium-Occupancy"


class OccupancyConnection(Connection):
    hasMedium: URIRef = Occupancy.node_type
    node_type = None


class OccupancyConnectionPoint(ConnectionPoint):
    hasMedium: URIRef = Occupancy.node_type
    node_type = None


class OccupancyInletConnectionPoint(OccupancyConnectionPoint, InletConnectionPoint):
    node_type = None


class OccupancyOutletConnectionPoint(OccupancyConnectionPoint, OutletConnectionPoint):
    node_type = None


class OccupancySystemConnectionPoint(SystemConnectionPoint):
    hasMedium: URIRef = Occupancy.node_type
    node_type = None


class OccupancyInletSystemConnectionPoint(
    OccupancySystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class OccupancyOutletSystemConnectionPoint(
    OccupancySystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


class OccupancyZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium: URIRef = Occupancy.node_type
    node_type = None


class OccupancyInletZoneConnectionPoint(
    OccupancyZoneConnectionPoint, InletZoneConnectionPoint
):
    node_type = None


class OccupancyOutletZoneConnectionPoint(
    OccupancyZoneConnectionPoint, OutletZoneConnectionPoint
):
    node_type = None
