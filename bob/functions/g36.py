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
)

g36 = bind_namespace("g36", "http://data.ashrae.org/standard223/1.0/extension/g36#")

_namespace = g36


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

    _class_iri = g36.FunctionBlock


class G36Figure_A_1(G36Sequence):
    zoneSetpointAdj: AnalogInput
    localOverride: BinaryInput
    zoneTemp: AnalogInput
    zoneCO2: AnalogInput
    zonewindowSwitch: BinaryInput
    zoneOccupancySensor: BinaryInput


class G36Figure_A_3(G36Figure_A_1):
    def __init__(self, comment=None, **kwargs):
        super().__init__(comment=comment, **kwargs)


class G36Figure_A_2(G36Figure_A_1):
    def __init__(self, comment=None, **kwargs):
        super().__init__(comment=comment, **kwargs)


class G36Figure_A_10(G36Sequence):
    def __init__(self, comment=None, **kwargs):
        super().__init__(comment=comment, **kwargs)

    _class_iri = g36.FunctionBlock
