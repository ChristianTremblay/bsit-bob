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
    Air,
    CompressedAir,
    SystemConnectionPoint,
    ZoneConnectionPoint,
    InletZoneConnectionPoint,
    OutletZoneConnectionPoint,
    BidirectionalSystemConnectionPoint,
)
from ..core import s223

__namespace__ = s223


class AirConnection(Connection):
    hasMedium: Medium = Air
    node_type = None


class AirConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Air
    node_type = None


class AirInletConnectionPoint(AirConnectionPoint, InletConnectionPoint):
    node_type = None


class AirOutletConnectionPoint(AirConnectionPoint, OutletConnectionPoint):
    node_type = None


class AirBidirectionalConnectionPoint(AirConnectionPoint, BidirectionalConnectionPoint):
    node_type = None


class AirSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Air
    node_type = None


class AirInletSystemConnectionPoint(
    AirSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class AirOutletSystemConnectionPoint(
    AirSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


class AirBidirectionalSystemConnectionPoint(
    AirSystemConnectionPoint, BidirectionalSystemConnectionPoint
):
    node_type = None


class AirZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium: Medium = Air
    node_type = None


class AirInletZoneConnectionPoint(AirZoneConnectionPoint, InletZoneConnectionPoint):
    node_type = None


class AirOutletZoneConnectionPoint(AirZoneConnectionPoint, OutletZoneConnectionPoint):
    node_type = None


class CompressedAirConnection(Connection):
    hasMedium: Medium = CompressedAir
    node_type = None


class CompressedAirConnectionPoint(ConnectionPoint):
    hasMedium: Medium = CompressedAir
    node_type = None


class CompressedAirInletConnectionPoint(
    CompressedAirConnectionPoint, InletConnectionPoint
):
    node_type = None


class CompressedAirOutletConnectionPoint(
    CompressedAirConnectionPoint, OutletConnectionPoint
):
    node_type = None


class CompressedAirSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = CompressedAir
    node_type = None


class CompressedAirInletSystemConnectionPoint(
    CompressedAirSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class CompressedAirOutletSystemConnectionPoint(
    CompressedAirSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None
