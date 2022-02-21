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
    SystemConnectionPoint,
    ZoneConnectionPoint,
    InletZoneConnectionPoint,
    OutletZoneConnectionPoint,
    BidirectionalSystemConnectionPoint,
)
from ..core import s223, enum
from ..signal import AnalogIn, AnalogOut

__namespace__ = s223

# === Light
class Light(Medium):
    node_type: URIRef = s223["Medium-Light"]
    label = "Medium-Light"


class LightConnection(Connection):
    hasMedium: URIRef = Light.node_type
    node_type = None


class LightConnectionPoint(ConnectionPoint):
    hasMedium: URIRef = Light.node_type
    node_type = None


class LightInletConnectionPoint(LightConnectionPoint, InletConnectionPoint):
    node_type = None


class LightOutletConnectionPoint(LightConnectionPoint, OutletConnectionPoint):
    node_type = None


class LightSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: URIRef = Light.node_type
    node_type = None


class LightInletSystemConnectionPoint(
    LightSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class LightOutletSystemConnectionPoint(
    LightSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


class LightZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium: URIRef = Light.node_type
    node_type = None


class LightInletZoneConnectionPoint(LightZoneConnectionPoint, InletZoneConnectionPoint):
    node_type = None


class LightOutletZoneConnectionPoint(
    LightZoneConnectionPoint, OutletZoneConnectionPoint
):
    node_type = None
