from .core import (
    ConnectionType,
    register_connection_type,
    Connection,
    Inlet,
    Outlet,
    Device,
)

from .signal import AnalogIn, AnalogOut


class Air(ConnectionType):
    connection_type: str = "Air"


@register_connection_type
class AirConnection(Air, Connection):
    pass


class AirInlet(Inlet, Air):
    pass


class AirOutlet(Outlet, Air):
    pass


class Fan(Device):
    ain: AirInlet
    aout: AirOutlet


class Damper(Device):
    ain: AirInlet
    aout: AirOutlet
    pos: AnalogIn


class AirFlowStation(Device):
    ain: AirInlet
    aout: AirOutlet
    flow = AnalogOut  # create an instance


class Zone(Device):
    sa: AirInlet  # supply air goes in
    ra: AirOutlet  # return air goes out


class OutsideAir(Device):
    oa: AirOutlet  # outside air goes in someplace
    ea: AirInlet  # from exhaust fan going out


class MixedAir(Device):
    oa: AirInlet  # outside air goes in someplace
    ra: AirInlet  # return air from the zone air goes in someplace
    ma: AirOutlet  # mixed air to become supply air to the zone
    ea: AirOutlet  # exhaust air going to the outside
