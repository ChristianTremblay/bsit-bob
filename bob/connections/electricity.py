from rdflib import URIRef
from .core import (
    s223,
    Substance,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    SystemConnectionPoint,
    InletSystemConnectionPoint,
    OutletSystemConnectionPoint,
    Device,
)
from ..signal import AnalogIn, AnalogOut

__namespace__ = s223


class Electricity(Substance):
    pass


class PowerConnection(Connection):
    hasSubstance = Electricity.node_type
    node_type = None


class PowerConnectionPoint(ConnectionPoint):
    hasSubstance = Electricity.node_type
    node_type = None


class PowerInletConnectionPoint(InletConnectionPoint, PowerConnectionPoint):
    node_type = None


class PowerOutletConnectionPoint(OutletConnectionPoint, PowerConnectionPoint):
    node_type = None


class ElectricalSystemConnectionPoint(SystemConnectionPoint):
    hasSubstance = Electricity.node_type
    node_type = None
