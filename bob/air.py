from rdflib import URIRef
from .core import (
    c223,
    Substance,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    SystemConnectionPoint,
    SystemInletConnectionPoint,
    SystemOutletConnectionPoint,
    Device,
)
from .signal import AnalogIn, AnalogOut

__namespace__ = c223


class Air(Substance):
    pass


class AirConnection(Connection):
    substance: URIRef = Air.node_type


class AirConnectionPoint(ConnectionPoint):
    substance: URIRef = Air.node_type


class AirInletConnectionPoint(AirConnectionPoint, InletConnectionPoint):
    pass


class AirOutletConnectionPoint(AirConnectionPoint, OutletConnectionPoint):
    pass


class AirSystemConnectionPoint(SystemConnectionPoint):
    node_type = None
    substance: URIRef = Air.node_type


class AirInletSystemConnectionPoint(
    AirSystemConnectionPoint, SystemInletConnectionPoint
):
    node_type = None


class AirOutletSystemConnectionPoint(
    AirSystemConnectionPoint, SystemOutletConnectionPoint
):
    node_type = None


class Fan(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint


class Damper(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    position = AnalogOut


class Filter(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    dp = AnalogOut


class AirFlowStation(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    flow = AnalogIn


class Zone(Device):
    supplyAirInlet: AirInletConnectionPoint  # supply air goes in
    returnAirOutlet: AirOutletConnectionPoint  # return air goes out
