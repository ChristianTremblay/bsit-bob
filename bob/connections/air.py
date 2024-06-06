from rdflib import URIRef

from ..core import (
    BOB,
    P223,
    S223,
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
)
from ..enum import Air

_namespace = BOB


class AirConnection(Connection):
    hasMedium: Medium = Air
    _class_iri = S223.Connection


class AirConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Air


class AirInletConnectionPoint(AirConnectionPoint, InletConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class AirOutletConnectionPoint(AirConnectionPoint, OutletConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class AirBidirectionalConnectionPoint(AirConnectionPoint, BidirectionalConnectionPoint):
    _class_iri = S223.BidirectionalConnectionPoint


class AirSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Air


class AirInletSystemConnectionPoint(
    AirSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class AirOutletSystemConnectionPoint(
    AirSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


class AirBidirectionalSystemConnectionPoint(
    AirSystemConnectionPoint, BidirectionalSystemConnectionPoint
):
    _class_iri = BOB.BidirectionalSystemConnectionPoint


class AirZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium: Medium = Air
    _class_iri = BOB.ZoneConnectionPoint


class AirInletZoneConnectionPoint(AirZoneConnectionPoint, InletZoneConnectionPoint):
    _class_iri = BOB.InletZoneConnectionPoint


class AirOutletZoneConnectionPoint(AirZoneConnectionPoint, OutletZoneConnectionPoint):
    _class_iri = BOB.OutletZoneConnectionPoint


class CompressedAirConnection(Connection):
    hasMedium = Air.CompressedAir
    _class_iri = S223.Connection


class CompressedAirConnectionPoint(ConnectionPoint):
    hasMedium = Air.CompressedAir


class CompressedAirInletConnectionPoint(
    CompressedAirConnectionPoint, InletConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class CompressedAirOutletConnectionPoint(
    CompressedAirConnectionPoint, OutletConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class CompressedAirSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Air.CompressedAir


class CompressedAirInletSystemConnectionPoint(
    CompressedAirSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class CompressedAirOutletSystemConnectionPoint(
    CompressedAirSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint
