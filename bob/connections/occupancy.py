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
    SystemConnectionPoint,
    ZoneConnectionPoint,
    bob,
    enum,
    p223,
    s223,
)

_namespace = bob


class OccupancyConnection(Connection):
    hasMedium: Medium
    _class_iri = s223.Connection


class OccupancyConnectionPoint(ConnectionPoint):
    hasMedium: Medium
    _class_iri = s223.ConnectionPoint


class OccupancyInletConnectionPoint(OccupancyConnectionPoint, InletConnectionPoint):
    _class_iri = s223.InletConnectionPoint


class OccupancyOutletConnectionPoint(OccupancyConnectionPoint, OutletConnectionPoint):
    _class_iri = s223.OutletConnectionPoint


class OccupancySystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium
    _class_iri = s223.SystemConnectionPoint


class OccupancyInletSystemConnectionPoint(
    OccupancySystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = s223.InletSystemConnectionPoint


class OccupancyOutletSystemConnectionPoint(
    OccupancySystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = s223.OutletSystemConnectionPoint


class OccupancyZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium: Medium
    _class_iri = s223.ZoneConnectionPoint


class OccupancyInletZoneConnectionPoint(
    OccupancyZoneConnectionPoint, InletZoneConnectionPoint
):
    _class_iri = s223.InletZoneConnectionPoint


class OccupancyOutletZoneConnectionPoint(
    OccupancyZoneConnectionPoint, OutletZoneConnectionPoint
):
    _class_iri = s223.OutletZoneConnectionPoint
