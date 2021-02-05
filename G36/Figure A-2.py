"""
Figure A-1
"""

from __future__ import annotations

from typing import Any

from bob import bind_model_namespace, dump

from bob.core import System, Device, Part
from bob.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from bob.hw import (
    HotWaterInlet,
    HotWaterOutlet,
    HotWaterSystemInlet,
    HotWaterSystemOutlet,
)
from bob.signal import AnalogIn, AnalogOut

from header import g36_header

__namespace__ = bind_model_namespace("ex", "urn:ex/")


class AirFlowStation(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    flow = AnalogIn


class DamperPositioner(Part):
    position = AnalogOut


class Damper(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    position: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a positioner
        self.damper_positioner = DamperPositioner(
            label=self.label + ".damper_positioner"
        )
        self > self.damper_positioner

        # reference the connections
        self.position = self.damper_positioner.position


class ValvePositioner(Part):
    position = AnalogOut


class HotWaterValve(Part):
    pass


class HotWaterCoil(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    hwInlet: HotWaterInlet
    hwOutlet: HotWaterOutlet
    valvePosition: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a positioner
        self.valve_positioner = ValvePositioner(label=self.label + ".damper_positioner")
        self > self.valve_positioner

        # create a hot water valve
        self.hot_water_valve = HotWaterValve(label=self.label + ".hot_water_valve")
        self > self.hot_water_valve

        # reference the properties
        self.valvePosition = self.valve_positioner.position


class VAV(System):
    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    airFlow: AnalogIn
    damperPosition: AnalogOut
    hwInlet: HotWaterSystemInlet
    hwOutlet: HotWaterSystemOutlet
    valvePosition: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create an air flow station
        self.air_flow_station = AirFlowStation(label=self.label + ".air_flow_station")
        self > self.air_flow_station

        # create a damper
        self.damper = Damper(label=self.label + ".damper")
        self > self.damper

        # create a hot water coil
        self.hot_water_coil = HotWaterCoil(label=self.label + ".hot_water_coil")
        self > self.hot_water_coil

        # link the air pieces together
        self.air_flow_station >> self.damper
        self.damper >> self.hot_water_coil

        # reference the connections
        self.airInlet > self.air_flow_station.airInlet
        self.airOutlet > self.hot_water_coil.airOutlet
        self.airFlow = self.air_flow_station.flow
        self.damperPosition = self.damper.position

        self.hwInlet >> self.hot_water_coil.hwInlet
        self.hwOutlet << self.hot_water_coil.hwOutlet
        self.valvePosition = self.hot_water_coil.valvePosition


# make one
vav = VAV(label="A-2")

g36_header("figure002")
dump()
