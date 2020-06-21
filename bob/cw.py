from typing import Any

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


class ChilledWaterValve(System):
    pos: AnalogIn
    cwin: ChilledWaterIn
    cwout: ChilledWaterOut


class ChilledWaterCoil(System):
    ain: AirIn
    aout: AirOut
    cws: ChilledWaterIn
    cwr: ChilledWaterOut


class ChilledWaterCoil2(ChilledWaterCoil):
    """
    This is an example of a chilled water coil that contains its valve as a
    subsystem and makes the valve position available as its own connection
    point.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a chilled water valve subsystem
        self.cw_valve = ChilledWaterValve(label=self.label + ".cw_valve")
        self > self.cw_valve

        # link the chilled water pieces together
        self.cw_valve >> self

        # lift the connection
        self.cw_valve_pos = self._connection_points["cw_valve_pos"] = self.cw_valve.pos
