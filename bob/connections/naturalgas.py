from rdflib import URIRef
from ..core import s223, enum

from ..core import (
    Medium,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    SystemConnectionPoint,
)
from ..signal import AnalogIn, AnalogOut

__namespace__ = enum


class NaturalGas(Medium):
    node_type: URIRef = enum.Medium_NaturalGas


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
