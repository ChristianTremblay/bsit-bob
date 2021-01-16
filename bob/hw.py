from typing import Any

from .core import (
    c223,
    ConnectionType,
    register_connection_type,
    Connection,
    InletConnectionPoint,
    OutletConnectionPoint,
    Device,
)
from .air import AirInletConnectionPoint, AirOutletConnectionPoint
from .signal import AnalogIn

__namespace__ = c223


class HotWater(ConnectionType):
    connection_type: str = "HotWater"


@register_connection_type
class HotWaterConnection(HotWater, Connection):
    pass


class HotWaterInlet(InletConnectionPoint, HotWater):
    pass


class HotWaterOutlet(OutletConnectionPoint, HotWater):
    pass


class HotWaterValve(Device):
    hotWaterInlet: HotWaterInlet
    hotWaterOutlet: HotWaterOutlet
    position = AnalogIn


class HotWaterCoil(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
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
