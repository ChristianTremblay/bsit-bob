from .core import ConnectionType, register_connection_type, Connection, In, Out, System

from .signal import AnalogIn, AnalogOut


class Air(ConnectionType):
    connection_type: str = "Air"


@register_connection_type
class AirConnection(Air, Connection):
    pass


class AirIn(In, Air):
    pass


class AirOut(Out, Air):
    pass


class Fan(System):
    ain: AirIn
    aout: AirOut


class Damper(System):
    ain: AirIn
    aout: AirOut
    pos: AnalogIn


class AirFlowStation(System):
    ain: AirIn
    aout: AirOut
    flow: AnalogOut


class Zone(System):
    sa: AirIn  # supply air goes in
    ra: AirOut  # return air goes out


class Outside(System):
    oa: AirOut  # outside air goes in someplace
    ea: AirOut  # from exhaust fan going out


class MixedAir(System):
    oa: AirIn  # outside air goes in someplace
    ra: AirIn  # return air from the zone air goes in someplace
    ma: AirOut  # mixed air to become supply air to the zone
    ea: AirOut  # exhaust air going to the outside
