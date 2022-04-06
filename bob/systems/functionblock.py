from rdflib import URIRef

from ..connections.air import (
    AirBidirectionalConnectionPoint,
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from ..core import (
    ExternalReference,
    InletConnectionPoint,
    Outlet,
    OutletConnectionPoint,
    Property,
    System,
    SystemConnectionPoint,
    enum,
    p223,
)
from ..property import ObservableProperty, QuantifiableObservableProperty

__namespace__ = p223


class FunctionBlockConnectionPoint(SystemConnectionPoint):
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


class FunctionBlock(System):
    """
    This building block is an abstraction of a function block
    which is any calculation or algorithm that interact with the
    model devices and systems.

    A function blocks works using sensors and their data and will
    provide more informations about properties, like information
    calculated from properties (think power based on current and voltage
    for example).

    Function block may also interact with device by providing the
    information about the commands to devices (ex. the modulation
    of a damper based on some algorithm) by the action of an output

    This block should be the gateway to align s223 with CDL.

    It can also abstract controllers and their logic.

    In s223, a function block is a black box. It's out of the scope
    to determine exactly what is going inside the block.

    A comment should be used to briefly explain the behaviour of the
    block.


    """

    node_type = p223.FunctionBlock
