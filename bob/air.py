from .core import (
    ConnectionType,
    register_connection_type,
    Connection,
    InletConnectionPoint,
    OutletConnectionPoint,
    Device,
)

from .signal import AnalogIn, AnalogOut


class Air(ConnectionType):
    connection_type: str = "Air"


@register_connection_type
class AirConnection(Air, Connection):
    pass


class AirInlet(InletConnectionPoint, Air):
    pass


class AirOutlet(OutletConnectionPoint, Air):
    pass


class Fan(Device):
    airInlet: AirInlet
    airOutlet: AirOutlet


class Damper(Device):
    airInlet: AirInlet
    airOutlet: AirOutlet
    position = AnalogOut


class Filter(Device):
    airInlet: AirInlet
    airOutlet: AirOutlet
    dp = AnalogOut


class AirFlowStation(Device):
    airInlet: AirInlet
    airOutlet: AirOutlet
    flow = AnalogIn


class Zone(Device):
    supplyAirInlet: AirInlet  # supply air goes in
    returnAirOutlet: AirOutlet  # return air goes out
