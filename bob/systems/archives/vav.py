from typing import Any

from bob.properties.flow import Flow
from bob.properties.ratio import Percent, PercentCommand

from ...connections.air import (
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from ...connections.water import (
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
)
from ...core import System, S223
from ...devices.hvac.airflowstation import AirFlowMonitor
from ...devices.hvac.coil import HotWaterCoil
from ...devices.hvac.damper import Damper
from ...devices.hvac.valve import TwoWayValve

_namespace = S223


class VAV1(System):
    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    airFlow: Flow
    damperPosition: Percent

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create an air flow station
        self.air_flow_station = AirFlowMonitor(label=self.label + ".air_flow_station")
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
    airFlow: Flow
    damperPosition: PercentCommand
    hwValvePosition: PercentCommand

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create an air flow station
        self.air_flow_station = AirFlowMonitor(label=self.label + ".air_flow_station")
        self > self.air_flow_station

        # create a damper
        self.damper = Damper(label=self.label + ".damper")
        self > self.damper

        # create a hot water coil
        self.hot_water_coil = HotWaterCoil(label=self.label + ".hw_coil")
        self > self.hot_water_coil

        # create a hot water valve
        self.hot_water_valve = TwoWayValve(
            label=self.label + ".hw_valve",
            waterInlet=HotWaterInletConnectionPoint,
            waterOutlet=HotWaterOutletConnectionPoint,
            hasPositionFeedback=0,
        )
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
        self.hwValvePosition = self.hot_water_valve.hasPositionFeedback
