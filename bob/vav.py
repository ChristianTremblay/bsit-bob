from typing import Any

from .core import c223, System
from .air import (
    AirFlowStation,
    Damper,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from .signal import AnalogIn, AnalogOut
from .hw import HotWaterCoil, HotWaterValve

__namespace__ = c223


class VAV1(System):
    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    airFlow: AnalogIn
    damperPosition: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create an air flow station
        self.air_flow_station = AirFlowStation(label=self.label + ".air_flow_station")
        self > self.air_flow_station

        # create a damper
        self.damper = Damper(label=self.label + ".damper")
        self > self.damper

        # link the air pieces together
        self.air_flow_station >> self.damper

        # reference the connections
        self.airInlet > self.air_flow_station.airInlet
        self.airOutlet < self.damper.airOutlet
        self.airFlow = self.air_flow_station.flow
        self.damperPosition = self.damper.position


class VAV2(System):
    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    airFlow: AnalogIn
    damperPosition: AnalogOut
    hwValvePosition: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create an air flow station
        self.air_flow_station = AirFlowStation(label=self.label + ".air_flow_station")
        self > self.air_flow_station

        # create a damper
        self.damper = Damper(label=self.label + ".damper")
        self > self.damper

        # create a hot water coil
        self.hot_water_coil = HotWaterCoil(label=self.label + ".hw_coil")
        self > self.hot_water_coil

        # create a hot water valve
        self.hot_water_valve = HotWaterValve(label=self.label + ".hw_valve")
        self > self.hot_water_valve

        # link them together
        self.air_flow_station.airOutlet >> self.damper.airInlet
        self.damper >> self.hot_water_coil

        # link the hot water pieces together
        self.hot_water_valve >> self.hot_water_coil

        # reference the connections
        self.airInlet > self.air_flow_station.airInlet
        self.airOutlet < self.hot_water_coil.airOutlet
        self.airFlow = self.air_flow_station.flow
        self.damperPosition = self.damper.position
        self.hwValvePosition = self.hot_water_valve.position
