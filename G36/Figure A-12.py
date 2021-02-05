"""
Figure A-12
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
    AirConnection,
)
from bob.cw import ChilledWaterCoil2
from bob.hw import HotWaterCoil2
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


class LinkedDampers(System):
    outsideAirInlet: AirInletSystemConnectionPoint
    returnAirInlet: AirInletSystemConnectionPoint
    mixedAirOutlet: AirOutletSystemConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.outside_air_damper = Damper(label=self.label + ".outside_air_damper")
        self > self.outside_air_damper
        self.outsideAirInlet > self.outside_air_damper.airInlet

        self.return_air_damper = Damper(label=self.label + ".return_air_damper")
        self > self.return_air_damper
        self.returnAirInlet > self.return_air_damper.airInlet

        self.mixedAirOutlet > self.outside_air_damper.airOutlet
        self.mixedAirOutlet > self.return_air_damper.airOutlet


class AHU(System):
    outsideAirInlet: AirInletSystemConnectionPoint
    supplyAirOutlet: AirOutletSystemConnectionPoint
    returnAirInlet: AirInletSystemConnectionPoint
    exhaustAirOutlet: AirOutletSystemConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create the linked dampers
        self.linked_dampers = LinkedDampers(label=self.label + ".linked_dampers")
        self.outsideAirInlet > self.linked_dampers.outsideAirInlet

        # create an air filter
        self.air_filter = AirFilter(label=self.label + ".air_filter")
        self.linked_dampers.mixedAirOutlet >> self.air_filter.airInlet

        # create a hot water coil
        self.hot_water_coil = HotWaterCoil2(label=self.label + ".hot_water_coil")
        self.air_filter >> self.hot_water_coil.airInlet

        # create a chilled water coil
        self.chilled_water_coil = ChilledWaterCoil2(
            label=self.label + ".chilled_water_coil"
        )
        self.hot_water_coil.airOutlet >> self.chilled_water_coil.airInlet

        # create a supply fan
        self.supply_fan = VFDFan(label=self.label + ".supply_fan")
        self.chilled_water_coil.airOutlet >> self.supply_fan.airInlet
        self.supplyAirOutlet > self.supply_fan.airOutlet

        # create a return fan
        self.return_fan = VFDFan(label=self.label + ".return_fan")
        self.returnAirInlet > self.return_fan.airInlet

        # create an exhaust air damper
        self.exhaust_air_damper = Damper(label=self.label + ".exhaust_air_damper")
        self.exhaustAirOutlet > self.exhaust_air_damper.airOutlet

        # air connection for outlet from return fan
        return_air = AirConnection(label=self.label + ".return_air")
        self.return_fan >> return_air
        return_air >> self.exhaust_air_damper
        return_air >> self.linked_dampers.returnAirInlet


# make one
vav = AHU(label="A-12")

g36_header("figure012")
dump()
