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
    _class_iri = None


class LightConnectionPoint(ConnectionPoint):
    _class_iri = None


class LightInletConnectionPoint(LightConnectionPoint, InletConnectionPoint):
    _class_iri = None


class LightOutletConnectionPoint(LightConnectionPoint, OutletConnectionPoint):
    _class_iri = None


class LightSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Light
    _class_iri = None


class LightInletSystemConnectionPoint(
    LightSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class LightOutletSystemConnectionPoint(
    LightSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


class LightZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium: Medium = Light
    _class_iri = None


class LightInletZoneConnectionPoint(LightZoneConnectionPoint, InletZoneConnectionPoint):
    _class_iri = None


class LightOutletZoneConnectionPoint(
    LightZoneConnectionPoint, OutletZoneConnectionPoint
):
    _class_iri = None


class LightVisibleConnection(Connection):
    hasMedium: Medium = LightVisible
    _class_iri = None


class LightVisibleConnectionPoint(ConnectionPoint):
    hasMedium: Medium = LightVisible
    _class_iri = None


class LightVisibleInletConnectionPoint(
    LightVisibleConnectionPoint, InletConnectionPoint
):
    _class_iri = None


class LightVisibleOutletConnectionPoint(
    LightVisibleConnectionPoint, OutletConnectionPoint
):
    _class_iri = None


class LightVisibleSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = LightVisible
    _class_iri = None


class LightVisibleInletSystemConnectionPoint(
    LightVisibleSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class LightVisibleOutletSystemConnectionPoint(
    LightVisibleSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


class LightVisibleZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium: Medium = LightVisible
    _class_iri = None


class LightVisibleInletZoneConnectionPoint(
    LightVisibleZoneConnectionPoint, InletZoneConnectionPoint
):
    _class_iri = None


class LightVisibleOutletZoneConnectionPoint(
    LightVisibleZoneConnectionPoint, OutletZoneConnectionPoint
):
    _class_iri = None
