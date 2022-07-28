from rdflib import URIRef

from ..core import (
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    Medium,
    NaturalGas,
    OutletConnectionPoint,
    SystemConnectionPoint,
    BOB,
    enum,
    P223,
    S223,
)

_namespace = BOB


class NaturalGasConnection(Connection):
    hasMedium: Medium = NaturalGas
    _class_iri = S223.Connection


class NaturalGasConnectionPoint(ConnectionPoint):
    hasMedium: Medium = NaturalGas


class NaturalGasInletConnectionPoint(InletConnectionPoint, NaturalGasConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class NaturalGasOutletConnectionPoint(OutletConnectionPoint, NaturalGasConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class NaturalGasSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = NaturalGas


class NaturalGasInletSystemConnectionPoint(
    InletConnectionPoint, NaturalGasSystemConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class NaturalGasOutletSystemConnectionPoint(
    OutletConnectionPoint, NaturalGasSystemConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint
