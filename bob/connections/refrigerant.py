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
from ..enum import RefrigerationGas

_namespace = BOB


class RefrigerationGasConnection(Connection):
    _volatile = ("hasMedium",)
    hasMedium: Medium = RefrigerationGas
    _class_iri = S223.Connection


class RefrigerationGasConnectionPoint(ConnectionPoint):
    _volatile = ("hasMedium",)
    hasMedium: Medium = RefrigerationGas


class RefrigerationGasInletConnectionPoint(
    InletConnectionPoint, RefrigerationGasConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class RefrigerationGasOutletConnectionPoint(
    OutletConnectionPoint, RefrigerationGasConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class RefrigerationGasBidirectionalConnectionPoint(
    BidirectionalConnectionPoint, RefrigerationGasConnectionPoint
):
    _class_iri = S223.BidirectionalConnectionPoint


class RefrigerationGasSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = RefrigerationGas


class RefrigerationGasInletSystemConnectionPoint(
    InletConnectionPoint, RefrigerationGasSystemConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class RefrigerationGasOutletSystemConnectionPoint(
    OutletConnectionPoint, RefrigerationGasSystemConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint
