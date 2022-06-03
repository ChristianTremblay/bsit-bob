from rdflib import URIRef

from ..core import (
    BidirectionalConnectionPoint,
    BidirectionalSystemConnectionPoint,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    InletZoneConnectionPoint,
    Light,
    Medium,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    OutletZoneConnectionPoint,
    SystemConnectionPoint,
    ZoneConnectionPoint,
    enum,
    s223,
)

_namespace = s223

LightVisible = Light("Visible")


# === Light
class LightVisibleConnection(Connection):
    hasMedium: Medium = Light
    node_type = None


class LightConnectionPoint(ConnectionPoint):
    node_type = None


class LightInletConnectionPoint(LightConnectionPoint, InletConnectionPoint):
    node_type = None


class LightOutletConnectionPoint(LightConnectionPoint, OutletConnectionPoint):
    node_type = None


class LightSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Light
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
    hasMedium: Medium = Light
    node_type = None


class LightInletZoneConnectionPoint(LightZoneConnectionPoint, InletZoneConnectionPoint):
    node_type = None


class LightOutletZoneConnectionPoint(
    LightZoneConnectionPoint, OutletZoneConnectionPoint
):
    node_type = None


class LightVisibleConnection(Connection):
    hasMedium: Medium = LightVisible
    node_type = None


class LightVisibleConnectionPoint(ConnectionPoint):
    hasMedium: Medium = LightVisible
    node_type = None


class LightVisibleInletConnectionPoint(
    LightVisibleConnectionPoint, InletConnectionPoint
):
    node_type = None


class LightVisibleOutletConnectionPoint(
    LightVisibleConnectionPoint, OutletConnectionPoint
):
    node_type = None


class LightVisibleSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = LightVisible
    node_type = None


class LightVisibleInletSystemConnectionPoint(
    LightVisibleSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class LightVisibleOutletSystemConnectionPoint(
    LightVisibleSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


class LightVisibleZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium: Medium = LightVisible
    node_type = None


class LightVisibleInletZoneConnectionPoint(
    LightVisibleZoneConnectionPoint, InletZoneConnectionPoint
):
    node_type = None


class LightVisibleOutletZoneConnectionPoint(
    LightVisibleZoneConnectionPoint, OutletZoneConnectionPoint
):
    node_type = None
