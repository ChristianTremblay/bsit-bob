"""
Figure A-11
"""

from __future__ import annotations

from typing import Any

from bob import bind_model_namespace, dump

from bob.core import System, Device, Part
from bob.air import (Fan, AirInletConnectionPoint, AirOutletConnectionPoint, AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,AirConnection, AirFlowStation)
from bob.hw import (HotWaterInlet, HotWaterOutlet, HotWaterSystemInlet,
    HotWaterSystemOutlet,)
from bob.signal import AnalogIn, AnalogOut, BinaryIn, BinaryOut

from header import g36_header

import logging

logging.basicConfig(level=logging.DEBUG)

__namespace__ = bind_model_namespace("ex", "urn:ex/")


class AirFilter(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    dp = AnalogIn


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


class VFD(Part):
    fanStatus = BinaryIn
    fanSpeedCommand = AnalogOut
    fanStart = BinaryOut


class VFDFan(Fan):
    # airInlet: AirInletConnectionPoint - inherits from Fan
    # airOutlet: AirOutletConnectionPoint - inherits from Fan
    fanStatus: BinaryIn
    fanSpeedCommand: AnalogOut
    fanStart: BinaryOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a positioner
        self.variable_frequency_drive = VFD(label=self.label + ".vfd")
        self > self.variable_frequency_drive

        # reference the properties
        self.fanStatus = self.variable_frequency_drive.fanStatus
        self.fanSpeedCommand = self.variable_frequency_drive.fanSpeedCommand
        self.fanStart = self.variable_frequency_drive.fanStart


logging.debug(f"VFDFan._nodes: {VFDFan._nodes}")


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
    returnAirInlet: AirInletSystemConnectionPoint
    returnAirFilterDP: AnalogIn
    supplyAirOutlet: AirOutletSystemConnectionPoint
    supplyAirDP: AnalogIn
    hwInlet: HotWaterSystemInlet
    hwOutlet: HotWaterSystemOutlet
    hwValvePosition: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create an air filter
        self.air_filter = AirFilter(label=self.label + ".air_filter")
        self.returnAirInlet > self.air_filter.airInlet
        self.returnAirFilterDP = self.air_filter.dp

        # create a hot water coil
        self.hot_water_coil = HotWaterCoil(label=self.label + ".hot_water_coil")
        self > self.hot_water_coil
        self.hwInlet > self.hot_water_coil.hwInlet
        self.hwOutlet > self.hot_water_coil.hwOutlet
        self.hwValvePosition = self.hot_water_coil.valvePosition

        # filter to hot water coil
        self.air_filter.airOutlet >> self.hot_water_coil.airInlet

        # create a fan with a variable frequency drive
        self.fan = VFDFan(label=self.label + ".fan")
        self > self.fan

        # link the air pieces together
        self.hot_water_coil >> self.fan
        self.supplyAirOutlet > self.fan.airOutlet


# make one
vav = VAV(label="A-11")

g36_header("figure011")
dump()
