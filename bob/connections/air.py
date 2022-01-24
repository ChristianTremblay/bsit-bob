from rdflib import URIRef

from ..node import (
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    Substance,
    SystemConnectionPoint,
)
from ..core import (
    s223,
)
from ..signal import AnalogIn, AnalogOut

__namespace__ = s223


class Air(Substance):
    pass


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
