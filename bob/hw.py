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
    hotWaterInlet: HotWaterInlet
    hotWaterOutlet: HotWaterOutlet
    position = AnalogIn


class HotWaterCoil(Device):
    airInlet: AirInlet
    airOutlet: AirOutlet
    hotWaterInlet: HotWaterInlet
    hotWaterOutlet: HotWaterOutlet


class HotWaterCoil2(HotWaterCoil):
    """
    This is an example of a hot water coil that contains its valve as a
    subsystem and makes the valve position available as its own connection
    point.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a hot water valve subsystem
        self.hot_water_valve = HotWaterValve(label=self.label + ".hw_valve")
        self > self.hot_water_valve

        # link the hot water pieces together
        self.hot_water_valve >> self

        # lift the connection
        self.hot_water_valve_pos = self.hot_water_valve.position
