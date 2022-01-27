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


class Electricity(Medium):
    node_type: URIRef = enum["Medium-Electricity"]


class ElectricalConnection(Connection):
    hasSubstance: URIRef = Electricity.node_type
    node_type = None


class ElectricalConnectionPoint(ConnectionPoint):
    hasSubstance: URIRef = Electricity.node_type
    node_type = None


class ElectricalInletConnectionPoint(InletConnectionPoint, ElectricalConnectionPoint):
    node_type = None


class ElectricalOutletConnectionPoint(OutletConnectionPoint, ElectricalConnectionPoint):
    node_type = None


class ElectricalSystemConnectionPoint(SystemConnectionPoint):
    hasSubstance: URIRef = Electricity.node_type
    node_type = None
