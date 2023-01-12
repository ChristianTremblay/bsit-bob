from rdflib import Literal, URIRef

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
    Medium,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    SystemConnectionPoint,
)

_namespace = P223


# === GENERAL

MechanicalCoupling = Medium("MechanicalCoupling", _alt_namespace=P223)


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
    _class_iri = BOB.InletSystemConnectionPoint


class MechanicalSystemOutletConnectionPoint(
    MechanicalSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint
