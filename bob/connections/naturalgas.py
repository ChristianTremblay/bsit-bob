from rdflib import URIRef

from ..core import (
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    Medium,
    NaturalGas,
    OutletConnectionPoint,
    SystemConnectionPoint,
    bob,
    enum,
    p223,
    s223,
)

_namespace = bob


class NaturalGasConnection(Connection):
    hasMedium: Medium = NaturalGas
    _class_iri = s223.Connection


class NaturalGasConnectionPoint(ConnectionPoint):
    hasMedium: Medium = NaturalGas
    _class_iri = s223.ConnectionPoint


class NaturalGasInletConnectionPoint(InletConnectionPoint, NaturalGasConnectionPoint):
    _class_iri = s223.InletConnectionPoint


class NaturalGasOutletConnectionPoint(OutletConnectionPoint, NaturalGasConnectionPoint):
    _class_iri = s223.OutletConnectionPoint


class NaturalGasSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = NaturalGas
    _class_iri = s223.SystemConnectionPoint


class NaturalGasInletSystemConnectionPoint(
    InletConnectionPoint, NaturalGasSystemConnectionPoint
):
    _class_iri = s223.InletConnectionPoint


class NaturalGasOutletSystemConnectionPoint(
    OutletConnectionPoint, NaturalGasSystemConnectionPoint
):
    _class_iri = s223.OutletConnectionPoint
