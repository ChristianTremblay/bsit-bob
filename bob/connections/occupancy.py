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
    _class_iri =None


class OccupancyConnectionPoint(ConnectionPoint):
    hasMedium: Medium = People
    _class_iri =None


class OccupancyInletConnectionPoint(OccupancyConnectionPoint, InletConnectionPoint):
    _class_iri =None


class OccupancyOutletConnectionPoint(OccupancyConnectionPoint, OutletConnectionPoint):
    _class_iri =None


class OccupancySystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = People
    _class_iri =None


class OccupancyInletSystemConnectionPoint(
    OccupancySystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri =None


class OccupancyOutletSystemConnectionPoint(
    OccupancySystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri =None


class OccupancyZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium: Medium = People
    _class_iri =None


class OccupancyInletZoneConnectionPoint(
    OccupancyZoneConnectionPoint, InletZoneConnectionPoint
):
    _class_iri =None


class OccupancyOutletZoneConnectionPoint(
    OccupancyZoneConnectionPoint, OutletZoneConnectionPoint
):
    _class_iri =None
