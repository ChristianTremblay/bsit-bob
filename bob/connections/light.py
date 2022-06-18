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
    bob,
    enum,
    p223,
    s223,
)

_namespace = bob

# === Light
class LightConnectionPoint(ConnectionPoint):
    _class_iri = s223.ConnectionPoint


class LightInletConnectionPoint(LightConnectionPoint, InletConnectionPoint):
    _class_iri = s223.ConnectionPoint


class LightOutletConnectionPoint(LightConnectionPoint, OutletConnectionPoint):
    _class_iri = s223.OutletConnectionPoint


class LightSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Light
    _class_iri = s223.SystemConnectionPoint


class LightInletSystemConnectionPoint(
    LightSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = s223.InletSystemConnectionPoint


class LightOutletSystemConnectionPoint(
    LightSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = s223.OutletSystemConnectionPoint


class LightZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium: Medium = Light
    _class_iri = s223.ZoneConnectionPoint


class LightInletZoneConnectionPoint(LightZoneConnectionPoint, InletZoneConnectionPoint):
    _class_iri = s223.InletZoneConnectionPoint


class LightOutletZoneConnectionPoint(
    LightZoneConnectionPoint, OutletZoneConnectionPoint
):
    _class_iri = s223.OutletZoneConnectionPoint


class LightVisibleConnection(Connection):
    hasMedium = Light.Visible
    _class_iri = s223.Connection


class LightVisibleConnectionPoint(ConnectionPoint):
    hasMedium = Light.Visible
    _class_iri = s223.ConnectionPoint


class LightVisibleInletConnectionPoint(
    LightVisibleConnectionPoint, InletConnectionPoint
):
    _class_iri = s223.InletConnectionPoint


class LightVisibleOutletConnectionPoint(
    LightVisibleConnectionPoint, OutletConnectionPoint
):
    _class_iri = s223.OutletConnectionPoint


class LightVisibleSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Light.Visible
    _class_iri = s223.SystemConnectionPoint


class LightVisibleInletSystemConnectionPoint(
    LightVisibleSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = s223.InletSystemConnectionPoint


class LightVisibleOutletSystemConnectionPoint(
    LightVisibleSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = s223.OutletSystemConnectionPoint


class LightVisibleZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium = Light.Visible
    _class_iri = s223.ZoneConnectionPoint


class LightVisibleInletZoneConnectionPoint(
    LightVisibleZoneConnectionPoint, InletZoneConnectionPoint
):
    _class_iri = s223.InletZoneConnectionPoint


class LightVisibleOutletZoneConnectionPoint(
    LightVisibleZoneConnectionPoint, OutletZoneConnectionPoint
):
    _class_iri = s223.OutletZoneConnectionPoint
