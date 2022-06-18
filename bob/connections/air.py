from rdflib import URIRef

from ..core import (
    Air,
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
    p223,
    s223,
)

_namespace = bob


class AirConnection(Connection):
    hasMedium: Medium = Air
    _class_iri = s223.Connection


class AirConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Air
    _class_iri = s223.ConnectionPoint


class AirInletConnectionPoint(AirConnectionPoint, InletConnectionPoint):
    _class_iri = s223.InletConnectionPoint


class AirOutletConnectionPoint(AirConnectionPoint, OutletConnectionPoint):
    _class_iri = s223.OutletConnectionPoint


class AirBidirectionalConnectionPoint(AirConnectionPoint, BidirectionalConnectionPoint):
    _class_iri = s223.BidirectionalConnectionPoint


class AirSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Air
    _class_iri = s223.SystemConnectionPoint


class AirInletSystemConnectionPoint(
    AirSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = s223.InletSystemConnectionPoint


class AirOutletSystemConnectionPoint(
    AirSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = s223.OutletSystemConnectionPoint


class AirBidirectionalSystemConnectionPoint(
    AirSystemConnectionPoint, BidirectionalSystemConnectionPoint
):
    _class_iri = s223.BidirectionalSystemConnectionPoint


class AirZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium: Medium = Air
    _class_iri = s223.ZoneConnectionPoint


class AirInletZoneConnectionPoint(AirZoneConnectionPoint, InletZoneConnectionPoint):
    _class_iri = s223.InletZoneConnectionPoint


class AirOutletZoneConnectionPoint(AirZoneConnectionPoint, OutletZoneConnectionPoint):
    _class_iri = s223.OutletZoneConnectionPoint


class CompressedAirConnection(Connection):
    hasMedium = Air.CompressedAir
    _class_iri = s223.Connection


class CompressedAirConnectionPoint(ConnectionPoint):
    hasMedium = Air.CompressedAir
    _class_iri = s223.ConnectionPoint


class CompressedAirInletConnectionPoint(
    CompressedAirConnectionPoint, InletConnectionPoint
):
    _class_iri = s223.InletConnectionPoint


class CompressedAirOutletConnectionPoint(
    CompressedAirConnectionPoint, OutletConnectionPoint
):
    _class_iri = s223.OutletConnectionPoint


class CompressedAirSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Air.CompressedAir
    _class_iri = s223.SystemConnectionPoint


class CompressedAirInletSystemConnectionPoint(
    CompressedAirSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = s223.InletSystemConnectionPoint


class CompressedAirOutletSystemConnectionPoint(
    CompressedAirSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = s223.OutletSystemConnectionPoint
