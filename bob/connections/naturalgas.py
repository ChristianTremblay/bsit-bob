from rdflib import URIRef

from ..core import (
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    Medium,
    NaturalGas,
    OutletConnectionPoint,
    SystemConnectionPoint,
    enum,
    s223,
)

_namespace = s223


class NaturalGasConnection(Connection):
    hasMedium: Medium = NaturalGas
    node_type = None


class NaturalGasConnectionPoint(ConnectionPoint):
    hasMedium: Medium = NaturalGas
    node_type = None


class NaturalGasInletConnectionPoint(InletConnectionPoint, NaturalGasConnectionPoint):
    node_type = None


class NaturalGasOutletConnectionPoint(OutletConnectionPoint, NaturalGasConnectionPoint):
    node_type = None


class NaturalGasSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = NaturalGas


class NaturalGasInletSystemConnectionPoint(
    InletConnectionPoint, NaturalGasSystemConnectionPoint
):
    node_type = None


class NaturalGasOutletSystemConnectionPoint(
    OutletConnectionPoint, NaturalGasSystemConnectionPoint
):
    node_type = None
