from .core import (
    c223,
    ConnectionType,
    register_connection_type,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    Device,
)
from .signal import AnalogIn, AnalogOut

__namespace__ = c223


class Air(ConnectionType):
    connection_type: str = "Air"


@register_connection_type
class AirConnection(Air, Connection):
    pass


class AirConnectionPoint(Air, ConnectionPoint):
    pass


class AirInletConnectionPoint(AirConnectionPoint, InletConnectionPoint):
    pass


class AirOutletConnectionPoint(AirConnectionPoint, OutletConnectionPoint):
    pass


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
