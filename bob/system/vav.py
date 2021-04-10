from typing import Any

from ..core import s223, System
from ..connections.air import (
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from ..signal import AnalogIn, AnalogOut
from ..devices.valve import HotWaterValve
from ..devices.htg_coil import HotWaterCoil
from ..devices.measuring import AirFlowStation
from ..devices.damper import Damper
__namespace__ = s223


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
        self.airInlet.mapsTo = self.air_flow_station.airInlet
        self.airOutlet.mapsTo = self.damper.airOutlet
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
        self.airInlet.mapsTo = self.air_flow_station.airInlet
        self.airOutlet.mapsTo = self.hot_water_coil.airOutlet
        self.airFlow = self.air_flow_station.flow
        self.damperPosition = self.damper.position
        self.hwValvePosition = self.hot_water_valve.position
