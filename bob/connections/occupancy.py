from rdflib import URIRef

from ..core import (
    BidirectionalConnectionPoint,
    BidirectionalSystemConnectionPoint,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    InletZoneConnectionPoint,
    Medium,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    OutletZoneConnectionPoint,
    People,
    SystemConnectionPoint,
    ZoneConnectionPoint,
    enum,
    s223,
)

_namespace = s223


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
