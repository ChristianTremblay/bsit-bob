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


class AirFlowStation(Device):
    airInlet: AirInlet
    airOutlet: AirOutlet
    flow = AnalogIn


class Zone(Device):
    supplyAirInlet: AirInlet  # supply air goes in
    returnAirOutlet: AirOutlet  # return air goes out


class OutsideAir(Device):
    outsideAir: AirOutlet  # outside air goes in someplace
    exhaustAir: AirInlet  # from exhaust fan going out


class MixedAir(Device):
    outsideAirInlet: AirInlet  # outside air goes in someplace
    returnAirInlet: AirInlet  # return air from the zone air goes in someplace
    mixedAirInlet: AirOutlet  # mixed air to become supply air to the zone
    exhaustAirOutlet: AirOutlet  # exhaust air going to the outside
