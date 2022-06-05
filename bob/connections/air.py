from rdflib import URIRef

from ..core import (
    Air,
    BidirectionalConnectionPoint,
    BidirectionalSystemConnectionPoint,
    CompressedAir,
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
    s223,
)

_namespace = s223


class AirConnection(Connection):
    hasMedium: Medium = Air
    _class_iri = None


class AirConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Air
    _class_iri = None


class AirInletConnectionPoint(AirConnectionPoint, InletConnectionPoint):
    _class_iri = None


class AirOutletConnectionPoint(AirConnectionPoint, OutletConnectionPoint):
    _class_iri = None


class AirBidirectionalConnectionPoint(AirConnectionPoint, BidirectionalConnectionPoint):
    _class_iri = None


class AirSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Air
    _class_iri = None


class AirInletSystemConnectionPoint(
    AirSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class AirOutletSystemConnectionPoint(
    AirSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


class AirBidirectionalSystemConnectionPoint(
    AirSystemConnectionPoint, BidirectionalSystemConnectionPoint
):
    _class_iri = None


class AirZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium: Medium = Air
    _class_iri = None


class AirInletZoneConnectionPoint(AirZoneConnectionPoint, InletZoneConnectionPoint):
    _class_iri = None


class AirOutletZoneConnectionPoint(AirZoneConnectionPoint, OutletZoneConnectionPoint):
    _class_iri = None


class CompressedAirConnection(Connection):
    hasMedium: Medium = CompressedAir
    _class_iri = None


class CompressedAirConnectionPoint(ConnectionPoint):
    hasMedium: Medium = CompressedAir
    _class_iri = None


class CompressedAirInletConnectionPoint(
    CompressedAirConnectionPoint, InletConnectionPoint
):
    _class_iri = None


class CompressedAirOutletConnectionPoint(
    CompressedAirConnectionPoint, OutletConnectionPoint
):
    _class_iri = None


class CompressedAirSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = CompressedAir
    _class_iri = None


class CompressedAirInletSystemConnectionPoint(
    CompressedAirSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class CompressedAirOutletSystemConnectionPoint(
    CompressedAirSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None
