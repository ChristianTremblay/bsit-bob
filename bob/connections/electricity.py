from rdflib import URIRef
from ..core import (
    s223,
)

from ..node import (
    Substance,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    SystemConnectionPoint,
)
from ..signal import AnalogIn, AnalogOut

__namespace__ = s223


class Electricity(Substance):
    pass


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
