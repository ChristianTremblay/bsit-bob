from rdflib import URIRef
from ..core import s223, enum

from ..core import (
    Medium,
    NaturalGas,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    SystemConnectionPoint,
)
from ..signal import AnalogIn, AnalogOut

__namespace__ = s223


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
