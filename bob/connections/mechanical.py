from rdflib import Literal, URIRef

from ..core import (
    P223,
    S223,
    BidirectionalConnectionPoint,
    BidirectionalSystemConnectionPoint,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    MechanicalCoupling,
    Medium,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    SystemConnectionPoint,
    enum,
)

_namespace = P223


# === GENERAL
class MechanicalConnection(Connection):
    hasMedium: Medium = MechanicalCoupling
    _class_iri = S223.Connection


class MechanicalConnectionPoint(ConnectionPoint):
    hasMedium: Medium = MechanicalCoupling


class MechanicalInletConnectionPoint(InletConnectionPoint, MechanicalConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class MechanicalOutletConnectionPoint(OutletConnectionPoint, MechanicalConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class MechanicalSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = MechanicalCoupling


class MechanicalSystemInletConnectionPoint(
    MechanicalSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class MechanicalSystemOutletConnectionPoint(
    MechanicalSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint
