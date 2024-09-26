from rdflib import URIRef

from ..core import (
    BOB,
    P223,
    S223,
    BidirectionalConnectionPoint,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    Medium,
    OutletConnectionPoint,
    SystemConnectionPoint,
    enum,
)
from ..enum import Refrigerant

_namespace = BOB


class RefrigerantConnection(Connection):
    _volatile = ("hasMedium",)
    hasMedium: Medium = Refrigerant
    _class_iri = S223.Connection


class RefrigerantConnectionPoint(ConnectionPoint):
    _volatile = ("hasMedium",)
    hasMedium: Medium = Refrigerant


class RefrigerantInletConnectionPoint(InletConnectionPoint, RefrigerantConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class RefrigerantOutletConnectionPoint(
    OutletConnectionPoint, RefrigerantConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class RefrigerantBidirectionalConnectionPoint(
    BidirectionalConnectionPoint, RefrigerantConnectionPoint
):
    _class_iri = S223.BidirectionalConnectionPoint


class RefrigerantSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Refrigerant


class RefrigerantInletSystemConnectionPoint(
    InletConnectionPoint, RefrigerantSystemConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class RefrigerantOutletSystemConnectionPoint(
    OutletConnectionPoint, RefrigerantSystemConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint
