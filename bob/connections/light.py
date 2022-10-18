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
    Light,
    Medium,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    OutletZoneConnectionPoint,
    SystemConnectionPoint,
    ZoneConnectionPoint,
    enum,
)

_namespace = BOB

# === Light
class LightConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Light


class LightInletConnectionPoint(LightConnectionPoint, InletConnectionPoint):
    pass


class LightOutletConnectionPoint(LightConnectionPoint, OutletConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class LightSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Light


class LightInletSystemConnectionPoint(
    LightSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class LightOutletSystemConnectionPoint(
    LightSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


class LightZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium: Medium = Light
    _class_iri = BOB.ZoneConnectionPoint


class LightInletZoneConnectionPoint(LightZoneConnectionPoint, InletZoneConnectionPoint):
    _class_iri = BOB.InletZoneConnectionPoint


class LightOutletZoneConnectionPoint(
    LightZoneConnectionPoint, OutletZoneConnectionPoint
):
    _class_iri = BOB.OutletZoneConnectionPoint


class LightVisibleConnection(Connection):
    hasMedium = Light.Visible
    _class_iri = S223.Connection


class LightVisibleConnectionPoint(ConnectionPoint):
    hasMedium = Light.Visible


class LightVisibleInletConnectionPoint(
    LightVisibleConnectionPoint, InletConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class LightVisibleOutletConnectionPoint(
    LightVisibleConnectionPoint, OutletConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class LightVisibleSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Light.Visible


class LightVisibleInletSystemConnectionPoint(
    LightVisibleSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class LightVisibleOutletSystemConnectionPoint(
    LightVisibleSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


class LightVisibleZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium = Light.Visible
    _class_iri = BOB.ZoneConnectionPoint


class LightVisibleInletZoneConnectionPoint(
    LightVisibleZoneConnectionPoint, InletZoneConnectionPoint
):
    _class_iri = BOB.InletZoneConnectionPoint


class LightVisibleOutletZoneConnectionPoint(
    LightVisibleZoneConnectionPoint, OutletZoneConnectionPoint
):
    _class_iri = BOB.OutletZoneConnectionPoint
