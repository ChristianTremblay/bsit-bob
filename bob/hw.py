from typing import Any

from .core import (
    s223,
    Substance,
    Connection,
    Device,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    System,
    SystemConnectionPoint,
    InletSystemConnectionPoint,
    OutletSystemConnectionPoint,
)
from .connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from .connections.water import (
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    HotWaterInletSystemConnectionPoint,
    HotWaterOutletSystemConnectionPoint,
)
from .signal import AnalogIn

__namespace__ = s223





class HotWaterValve(Device):
    hotWaterInlet: HotWaterInletConnectionPoint
    hotWaterOutlet: HotWaterOutletConnectionPoint
    position = AnalogIn


class HotWaterCoil(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    hotWaterInlet: HotWaterInletConnectionPoint
    hotWaterOutlet: HotWaterOutletConnectionPoint


class HotWaterBoiler(Device):
    hotWaterSupply: HotWaterInletConnectionPoint
    hotWaterReturn: HotWaterOutletConnectionPoint


class HotWaterCoil2(System):
    """
    This is an example of a hot water coil that contains its valve as a
    subsystem and makes the valve position available as its own connection
    point.
    """

    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    hotWaterInlet: HotWaterInletSystemConnectionPoint
    hotWaterOutlet: HotWaterOutletSystemConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a hot water coil
        self.hot_water_coil = HotWaterCoil(label=self.label + ".hw_coil")
        self.airInlet.mapsTo = self.hot_water_coil.airInlet
        self.airOutlet.mapsTo = self.hot_water_coil.airOutlet

        # create a hot water valve
        self.hot_water_valve = HotWaterValve(label=self.label + ".hw_valve")
        self.hotWaterInlet.mapsTo = self.hot_water_valve.hotWaterInlet
        self.hot_water_valve >> self.hot_water_coil
        self.hotWaterOutlet.mapsTo = self.hot_water_coil.hotWaterOutlet

        # reference the valve position
        self.hot_water_valve_pos = self.hot_water_valve.position
