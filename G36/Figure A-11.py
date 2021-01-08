"""
Figure A-11
"""

from __future__ import annotations

from typing import Any

from bob import bind_model_namespace, dump

from bob.core import System, Device, Part
from bob.air import Fan, AirInlet, AirOutlet, AirConnection, AirFlowStation
from bob.hw import HotWaterInlet, HotWaterOutlet
from bob.signal import AnalogIn, AnalogOut, BinaryIn, BinaryOut

from header import g36_header

import logging

logging.basicConfig(level=logging.DEBUG)

__namespace__ = bind_model_namespace("ex", "urn:ex/")


class AirFilter(Device):
    airInlet: AirInlet
    airOutlet: AirOutlet
    dp = AnalogIn


class DamperPositioner(Part):
    position = AnalogOut


class Damper(Device):
    airInlet: AirInlet
    airOutlet: AirOutlet
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
    airInlet: AirInlet  ## bug
    airOutlet: AirOutlet  ## bug
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
    airInlet: AirInlet
    airOutlet: AirOutlet
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
    supplyAirInlet: AirInlet
    returnAirInlet: AirInlet
    supplyAirOutlet: AirOutlet
    supplyAirFlow: AnalogIn
    damperPosition: AnalogOut
    hwInlet: HotWaterInlet
    hwOutlet: HotWaterOutlet
    hwValvePosition: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create an air flow station
        self.air_flow_station = AirFlowStation(label=self.label + ".air_flow_station")
        self > self.air_flow_station
        self.supplyAirInlet >> self.air_flow_station.airInlet
        self.supplyAirFlow = self.air_flow_station.flow

        # create a damper
        self.damper = Damper(label=self.label + ".damper")
        self > self.damper
        self.damperPosition = self.damper.position

        # create a hot water coil
        self.hot_water_coil = HotWaterCoil(label=self.label + ".hot_water_coil")
        self > self.hot_water_coil
        self.hwInlet >> self.hot_water_coil.hwInlet
        self.hwOutlet << self.hot_water_coil.hwOutlet
        self.hwValvePosition = self.hot_water_coil.valvePosition
        self.returnAirInlet >> self.hot_water_coil.airInlet

        # create a fan with a variable frequency drive
        self.fan = VFDFan(label=self.label + ".fan")
        self > self.fan

        # connection for merge
        merged_air = AirConnection(label=self.label + ".merge")

        # link the air pieces together
        self.damper.airOutlet >> merged_air
        self.fan >> merged_air
        merged_air >> self.supplyAirOutlet


# make one
vav = VAV(label="A-11")

g36_header("figure011")
dump()
