from rdflib import URIRef

from ...systems.functionblock import FunctionBlock
from ...connections.air import (
    AirBidirectionalConnectionPoint,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from ...core import (
    ExternalReference,
    InletConnectionPoint,
    Outlet,
    OutletConnectionPoint,
    System,
    p223,
    enum,
    Property,
    SystemConnectionPoint,
    bind_namespace,
)
from ...property import ObservableProperty, QuantifiableObservableProperty

g36 = bind_namespace("g36", "http://data.ashrae.org/standard223/1.0/extension/g36#")

__namespace__ = g36


class G36BlockConnectionPoint(SystemConnectionPoint):
    pass
    # find medium...


class AnalogIn(SystemConnectionPoint, InletConnectionPoint):
    hasExternalReference: ExternalReference


class AnalogOut(SystemConnectionPoint, OutletConnectionPoint):
    hasExternalReference: ExternalReference


class BinaryIn(SystemConnectionPoint, InletConnectionPoint):
    hasExternalReference: ExternalReference


class BinaryOut(SystemConnectionPoint, OutletConnectionPoint):
    hasExternalReference: ExternalReference


class G36Block(FunctionBlock):
    """
    This function is a subclass of a Function Block kept
    in the namespace of G36

    In Guideline 36, models present the notion of AI, AO, BI, BO
    and those concept can be modeled using a Function block.
    Function block is then an abstraction of the sequence of
    operation suggested by G36.

    """

    node_type = g36.FunctionBlock
