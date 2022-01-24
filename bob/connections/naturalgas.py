from rdflib import URIRef
from ..core import (
    s223,
)

from ..node import (
    Substance,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    SystemConnectionPoint,
)
from ..signal import AnalogIn, AnalogOut

__namespace__ = s223


class NaturalGas(Substance):
    pass


class NaturalGasConnection(Connection):
    hasSubstance: URIRef = NaturalGas.node_type
    node_type = None


class NaturalGasConnectionPoint(ConnectionPoint):
    hasSubstance: URIRef = NaturalGas.node_type
    node_type = None


class NaturalGasInletConnectionPoint(InletConnectionPoint, NaturalGasConnectionPoint):
    node_type = None


class NaturalGasOutletConnectionPoint(OutletConnectionPoint, NaturalGasConnectionPoint):
    node_type = None


class NaturalGasSystemConnectionPoint(SystemConnectionPoint):
    hasSubstance: URIRef = NaturalGas.node_type


class NaturalGasInletSystemConnectionPoint(
    InletConnectionPoint, NaturalGasSystemConnectionPoint
):
    node_type = None


class NaturalGasOutletSystemConnectionPoint(
    OutletConnectionPoint, NaturalGasSystemConnectionPoint
):
    node_type = None
