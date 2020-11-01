from typing import Any

from .core import (
    ConnectionType,
    register_connection_type,
    Connection,
    Inlet,
    Outlet,
    Device,
)
from .air import AirInlet, AirOutlet
from .signal import AnalogIn


class HotWater(ConnectionType):
    connection_type: str = "HotWater"


@register_connection_type
class HotWaterConnection(HotWater, Connection):
    pass


class HotWaterInlet(Inlet, HotWater):
    pass


class HotWaterOutlet(Outlet, HotWater):
    pass


class HotWaterValve(Device):
    hwin: HotWaterInlet
    hwout: HotWaterOutlet
    pos = AnalogIn


class HotWaterCoil(Device):
    ain: AirInlet
    aout: AirOutlet
    hws: HotWaterInlet
    hwr: HotWaterOutlet


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
        self.hw_valve_pos = self.hw_valve.pos
