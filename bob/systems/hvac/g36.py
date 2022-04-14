from rdflib import URIRef

from bob.connections.electricity import (
    ModulationSignalSystemInletConnectionPoint,
    ModulationSignalSystemOutletConnectionPoint,
    OnOffSignalSystemInletConnectionPoint,
    OnOffSignalSystemOutletConnectionPoint,
)

from ...connections.air import (
    AirBidirectionalConnectionPoint,
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from ...core import (
    ExternalReference,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    Outlet,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    Property,
    System,
    SystemConnectionPoint,
    bind_namespace,
    enum,
    p223,
)
from ...functions import (
    AnalogInput,
    AnalogOutput,
    BinaryInput,
    BinaryOutput,
    FunctionBlock,
)
from ...property import ObservableProperty, QuantifiableObservableProperty

g36 = bind_namespace("g36", "http://data.ashrae.org/standard223/1.0/extension/g36#")

__namespace__ = g36


class AnalogIn(AnalogInput):
    node_type = g36.AnalogIn


class AnalogOut(AnalogOutput):
    node_type = g36.AnalogOut


class BinaryIn(BinaryInput):
    node_type = g36.BinaryIn


class BinaryOut(BinaryOutput):
    node_type = g36.BinaryOut


class G36Block(FunctionBlock):
    """
    This function is a subclass of a Function Block kept
    in the namespace of G36.

    In Guideline 36, models present the notion of AI, AO, BI, BO
    and those concept can be modeled using a Function block.
    Function block is then an abstraction of the sequence of
    operation suggested by G36.

    Comment of this block is the description of the sequence.
    """

    node_type = g36.FunctionBlock
