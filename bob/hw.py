from typing import Any

from .core import (
    c223,
    ConnectionType,
    register_connection_type,
    Connection,
    Device,
    InletConnectionPoint,
    OutletConnectionPoint,
    System,
    SystemInletConnectionPoint,
    SystemOutletConnectionPoint,
)
from .air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)

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


class HotWaterSystemInlet(SystemInletConnectionPoint, HotWater):
    pass


class HotWaterSystemOutlet(SystemOutletConnectionPoint, HotWater):
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


class HotWaterBoiler(Device):
    hotWaterSupply: HotWaterInlet
    hotWaterReturn: HotWaterOutlet


class HotWaterCoil2(System):
    """
    This is an example of a hot water coil that contains its valve as a
    subsystem and makes the valve position available as its own connection
    point.
    """

    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    hotWaterInlet: HotWaterSystemInlet
    hotWaterOutlet: HotWaterSystemOutlet

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a hot water coil
        self.hot_water_coil = HotWaterCoil(label=self.label + ".hw_coil")
        self.airInlet > self.hot_water_coil.airInlet
        self.airOutlet > self.hot_water_coil.airOutlet

        # create a hot water valve
        self.hot_water_valve = HotWaterValve(label=self.label + ".hw_valve")
        self.hotWaterInlet > self.hot_water_valve.hotWaterInlet
        self.hot_water_valve >> self.hot_water_coil
        self.hotWaterOutlet > self.hot_water_coil.hotWaterOutlet

        # reference the valve position
        self.hot_water_valve_pos = self.hot_water_valve.position
