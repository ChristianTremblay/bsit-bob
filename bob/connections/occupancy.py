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
    People,
    SystemConnectionPoint,
    ZoneConnectionPoint,
    InletZoneConnectionPoint,
    OutletZoneConnectionPoint,
    BidirectionalSystemConnectionPoint,
)
from ..core import s223, enum
from ..signal import AnalogIn, AnalogOut

__namespace__ = s223

class OccupancyConnection(Connection):
    hasMedium: Medium = People
    node_type = None


class OccupancyConnectionPoint(ConnectionPoint):
    hasMedium: Medium = People
    node_type = None


class OccupancyInletConnectionPoint(OccupancyConnectionPoint, InletConnectionPoint):
    node_type = None


class OccupancyOutletConnectionPoint(OccupancyConnectionPoint, OutletConnectionPoint):
    node_type = None


class OccupancySystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = People
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
    hasMedium: Medium = People
    node_type = None


class OccupancyInletZoneConnectionPoint(
    OccupancyZoneConnectionPoint, InletZoneConnectionPoint
):
    node_type = None


class OccupancyOutletZoneConnectionPoint(
    OccupancyZoneConnectionPoint, OutletZoneConnectionPoint
):
    node_type = None
