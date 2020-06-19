from .core import ConnectionType, register_connection_type, Connection, In, Out, System

from .air import AirIn, AirOut
from .signal import AnalogIn


class HotWater(ConnectionType):
    connection_type: str = "HotWater"


@register_connection_type
class HotWaterConnection(HotWater, Connection):
    pass


class HotWaterIn(In, HotWater):
    pass


class HotWaterOut(Out, HotWater):
    pass


class HotWaterCoil(System):
    ain: AirIn
    aout: AirOut
    hws: HotWaterIn
    hwr: HotWaterOut


class HotWaterValve(System):
    pos: AnalogIn
    hwin: HotWaterIn
    hwout: HotWaterOut
