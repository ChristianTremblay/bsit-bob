"""
Figure A-6
"""

from __future__ import annotations

from typing import Any

from bob import bind_model_namespace, dump

from bob.core import System, Device, Part
from bob.air import (
    Fan,
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
from bob.signal import AnalogIn, AnalogOut, BinaryOut

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


class ECMFan(Fan):
    # airInlet: AirInletConnectionPoint
    # airOutlet: AirOutletConnectionPoint
    pass


class ECM(Part):
    fanStart = BinaryOut
    fanSpeedFeedback = AnalogIn
    fanSpeedCommand = AnalogOut


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
    supplyAirInlet: AirInletSystemConnectionPoint
    returnAirInlet: AirInletSystemConnectionPoint
    supplyAirOutlet: AirOutletSystemConnectionPoint
    supplyAirFlow: AnalogIn
    damperPosition: AnalogOut
    hwInlet: HotWaterSystemInlet
    hwOutlet: HotWaterSystemOutlet
    hwValvePosition: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create an air flow station
        self.air_flow_station = AirFlowStation(label=self.label + ".air_flow_station")
        self > self.air_flow_station
        self.supplyAirInlet > self.air_flow_station.airInlet
        self.supplyAirFlow = self.air_flow_station.flow

        # create a damper
        self.damper = Damper(label=self.label + ".damper")
        self > self.damper
        self.damperPosition = self.damper.position

        # create a fan with an ECM part
        self.fan = ECMFan(label=self.label + ".fan")
        self.fan_ecm = ECM(label=self.label + ".fan.ecm")
        self > self.fan > self.fan_ecm

        # create a hot water coil
        self.hot_water_coil = HotWaterCoil(label=self.label + ".hot_water_coil")
        self > self.hot_water_coil
        self.hwInlet > self.hot_water_coil.hwInlet
        self.hwOutlet > self.hot_water_coil.hwOutlet
        self.hwValvePosition = self.hot_water_coil.valvePosition

        # fan output goes to the hot water coil
        self.fan >> self.hot_water_coil
        self.supplyAirOutlet > self.hot_water_coil.airOutlet

        # merge the inlets together
        self.returnAirInlet > self.damper.airOutlet
        self.returnAirInlet > self.fan.airInlet


# make one
vav = VAV(label="A-6")

g36_header("figure006")
dump()
