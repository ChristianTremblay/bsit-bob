from .core import ConnectionType, register_connection_type, Connection, In, Out, System

from .air import AirIn, AirOut
from .signal import AnalogIn


class ChilledWater(ConnectionType):
    connection_type: str = "ChilledWater"


@register_connection_type
class ChilledWaterConnection(ChilledWater, Connection):
    pass


class ChilledWaterIn(In, ChilledWater):
    pass


class ChilledWaterOut(Out, ChilledWater):
    pass


class ChilledWaterCoil(System):
    ain: AirIn
    aout: AirOut
    cws: ChilledWaterIn
    cwr: ChilledWaterOut


class ChilledWaterValve(System):
    signal: AnalogIn
    cwin: ChilledWaterIn
    cwout: ChilledWaterOut
