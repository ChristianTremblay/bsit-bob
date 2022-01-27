from rdflib import URIRef

from ..core import (
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    Medium,
    SystemConnectionPoint,
)
from ..core import s223, enum
from ..signal import AnalogIn, AnalogOut

__namespace__ = enum

# === AIR
class Air(Medium):
    node_type: URIRef = enum.Medium_Air


class AirConnection(Connection):
    hasSubstance: URIRef = Air.node_type
    node_type = None


class AirConnectionPoint(ConnectionPoint):
    hasSubstance: URIRef = Air.node_type
    node_type = None


class AirInletConnectionPoint(AirConnectionPoint, InletConnectionPoint):
    node_type = None


class AirOutletConnectionPoint(AirConnectionPoint, OutletConnectionPoint):
    node_type = None


class AirSystemConnectionPoint(SystemConnectionPoint):
    hasSubstance: URIRef = Air.node_type
    node_type = None


class AirInletSystemConnectionPoint(
    AirSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class AirOutletSystemConnectionPoint(
    AirSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


# === COMPRESSED AIR
class CompressedAir(Medium):
    node_type: URIRef = enum.Medium_CompressedAir


class CompressedAirConnection(Connection):
    hasSubstance: URIRef = CompressedAir.node_type
    node_type = None


class CompressedAirConnectionPoint(ConnectionPoint):
    hasSubstance: URIRef = CompressedAir.node_type
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
    hasSubstance: URIRef = CompressedAir.node_type
    node_type = None


class CompressedAirInletSystemConnectionPoint(
    CompressedAirSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class CompressedAirOutletSystemConnectionPoint(
    CompressedAirSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None
