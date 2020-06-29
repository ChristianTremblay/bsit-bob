from typing import Any

from .core import ConnectionType, register_connection_type, Connection, In, Out, System
from .air import AirIn, AirOut
from .signal import AnalogIn


class HotWater(ConnectionType):
    __brick__: "Hot_Water"
    connection_type: str = "HotWater"


@register_connection_type
class HotWaterConnection(HotWater, Connection):
    pass


class HotWaterIn(In, HotWater):
    pass


class HotWaterOut(Out, HotWater):
    pass


class HotWaterValve(System):
    __brick__: "Hot_Water_Valve"
    pos: AnalogIn
    hwin: HotWaterIn
    hwout: HotWaterOut


class HotWaterCoil(System):
    __brick__: "Hot_Water_Coil"
    ain: AirIn
    aout: AirOut
    hws: HotWaterIn
    hwr: HotWaterOut


class HotWaterCoil2(HotWaterCoil):
    """
    This is an example of a hot water coil that contains its valve as a
    subsystem and makes the valve position available as its own connection
    point.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a hot water valve subsystem
        self.hw_valve = HotWaterValve(label=self.label + ".hw_valve")
        self > self.hw_valve

        # link the hot water pieces together
        self.hw_valve >> self

        # lift the connection
        self.hw_valve_pos = self._connection_points["hw_valve_pos"] = self.hw_valve.pos
