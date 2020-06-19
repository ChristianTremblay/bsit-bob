from typing import Any

from .core import ConnectionType, register_connection_type, Connection, In, Out, System

from .air import AirFlowStation, Damper
from .hw import HotWaterCoil, HotWaterValve
from .signal import AnalogOut


class VAV1(System):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create an air flow station and damper
        self.air_flow_station = AirFlowStation()
        self > self.air_flow_station

        self.damper = Damper()
        self > self.damper

        # link the air pieces together, the tool notices that the air flow
        # station flow output could be connected to the damper position so
        # the simplest (self.air_flow_station >> self.damper) is an error
        self.air_flow_station.aout >> self.damper.ain

        # lift the connections
        self.ain = self._connection_points["ain"] = self.air_flow_station.ain
        self.aout = self._connection_points["aout"] = self.damper.aout
        self.flow = self._connection_points["flow"] = self.air_flow_station.flow
        self.damper_pos = self._connection_points["damper_pos"] = self.damper.pos


class VAV2(System):
    temp: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create an air flow station
        self.air_flow_station = AirFlowStation()
        self > self.air_flow_station

        # create a damper
        self.damper = Damper()
        self > self.damper

        # create a hot water coil
        self.hw_coil = HotWaterCoil()
        self > self.hw_coil

        # create a hot water valve
        self.hw_valve = HotWaterValve()
        self > self.hw_valve

        # link the air pieces together, the tool notices that the air flow
        # station flow output could be connected to the damper position so
        # the simplest (self.air_flow_station >> self.damper) is an error
        self.air_flow_station.aout >> self.damper.ain
        self.damper >> self.hw_coil

        # link the hot water pieces together
        self.hw_valve >> self.hw_coil

        # lift the connections
        self.ain = self._connection_points["ain"] = self.air_flow_station.ain
        self.aout = self._connection_points["aout"] = self.hw_coil.aout
        self.flow = self._connection_points["flow"] = self.air_flow_station.flow
        self.damper_pos = self._connection_points["damper_pos"] = self.damper.pos
        self.hw_valve_pos = self._connection_points["hw_valve_pos"] = self.hw_valve.pos
