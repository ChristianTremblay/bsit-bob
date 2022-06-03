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


class G36Figure_A_1(G36Sequence):
    def __init__(self, comment=None, **kwargs):
        if not comment:
            raise ValueError("Must provide sequence of operation as comment")
        super().__init__(comment=comment, **kwargs)
        self.zoneSetpointAdj = AnalogIn(
            label="Zone Setpoint Adjust", function_block=self
        )
        self.LocalOverride = BinaryIn(label="Local Override", function_block=self)
        self.zoneTemp = AnalogIn(label="Zone Temp", function_block=self)
        self.zoneCO2 = AnalogIn(label="Zone CO2", function_block=self)
        self.zonewindowSwitch = BinaryIn(
            label="Zone Window Switch", function_block=self
        )
        self.zoneOccupancySensor = BinaryIn(
            label="Zone Occupancy Sensor", function_block=self
        )


class G36Figure_A_3(G36Figure_A_1):
    def __init__(self, comment=None, **kwargs):
        super().__init__(comment=comment, **kwargs)


class G36Figure_A_2(G36Figure_A_1):
    def __init__(self, comment=None, **kwargs):
        super().__init__(comment=comment, **kwargs)


class G36Figure_A_10(G36Sequence):
    def __init__(self, comment=None, **kwargs):
        super().__init__(comment=comment, **kwargs)
