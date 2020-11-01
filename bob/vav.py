from typing import Any

from .core import Device
from .air import AirFlowStation, Damper
from .hw import HotWaterCoil, HotWaterValve
from .signal import AnalogOut


class VAV1(Device):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create an air flow station
        self.air_flow_station = AirFlowStation(label=self.label + ".air_flow_station")
        self > self.air_flow_station

        # create a damper
        self.damper = Damper(label=self.label + ".damper")
        self > self.damper

        # link the air pieces together, the tool notices that the air flow
        # station flow output could be connected to the damper position so
        # the simplest (self.air_flow_station >> self.damper) is an error
        self.air_flow_station.airOutlet >> self.damper.airInlet

        # lift the connections
        self.airInlet = self._connection_points[
            "airInlet"
        ] = self.air_flow_station.airInlet
        self.airOutlet = self._connection_points["airOutlet"] = self.damper.airOutlet
        self.flow = self.air_flow_station.flow
        self.damper_pos = self.damper.pos


class VAV2(Device):
    temp: AnalogOut

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

        # lift the connections
        self.airInlet = self._connection_points[
            "airInlet"
        ] = self.air_flow_station.airInlet
        self.airOutlet = self._connection_points[
            "airOutlet"
        ] = self.hot_water_coil.airOutlet
        self.flow = self.air_flow_station.flow
        self.damper_pos = self.damper.pos
        self.hot_water_valve_pos = self.hot_water_valve.pos
