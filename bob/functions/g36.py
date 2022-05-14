from ..connections.electricity import (
    ModulationSignalSystemInletConnectionPoint,
    ModulationSignalSystemOutletConnectionPoint,
    OnOffSignalSystemInletConnectionPoint,
    OnOffSignalSystemOutletConnectionPoint,
)
from ..core import Node, PropertyReference, bind_namespace
from ..properties import OccupancyStatus, Schedule
from ..property import ObservableProperty, QuantifiableObservableProperty
from . import (
    AnalogInput,
    AnalogOutput,
    BinaryInput,
    BinaryOutput,
    FunctionBlock,
    InputConnector,
    OutputConnector,
)

g36 = bind_namespace("g36", "http://data.ashrae.org/standard223/1.0/extension/g36#")

_namespace = g36


class AnalogIn(InputConnector):
    node_type = g36.AnalogIn


class AnalogOut(OutputConnector):
    node_type = g36.AnalogOut


class BinaryIn(InputConnector):
    node_type = g36.BinaryIn


class BinaryOut(OutputConnector):
    node_type = g36.BinaryOut


class G36Sequence(FunctionBlock):
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
