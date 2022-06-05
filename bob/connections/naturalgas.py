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
from ..signal import AnalogIn, AnalogOut

_namespace = s223


class NaturalGasConnection(Connection):
    hasMedium: Medium = NaturalGas
    _class_iri = None


class NaturalGasConnectionPoint(ConnectionPoint):
    hasMedium: Medium = NaturalGas
    _class_iri = None


class NaturalGasInletConnectionPoint(InletConnectionPoint, NaturalGasConnectionPoint):
    _class_iri = None


class NaturalGasOutletConnectionPoint(OutletConnectionPoint, NaturalGasConnectionPoint):
    _class_iri = None


class NaturalGasSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = NaturalGas


class NaturalGasInletSystemConnectionPoint(
    InletConnectionPoint, NaturalGasSystemConnectionPoint
):
    _class_iri = None


class NaturalGasOutletSystemConnectionPoint(
    OutletConnectionPoint, NaturalGasSystemConnectionPoint
):
    _class_iri = None
