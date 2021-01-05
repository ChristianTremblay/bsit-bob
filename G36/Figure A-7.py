"""
Figure A-7
"""

from __future__ import annotations

from typing import Any

from bob import bind_model_namespace, dump

from bob.core import System, Device, Part
from bob.air import Fan, AirInlet, AirOutlet, AirConnection
from bob.hw import HotWaterInlet, HotWaterOutlet
from bob.signal import AnalogIn, AnalogOut, BinaryOut

from header import g36_header

__namespace__ = bind_model_namespace("ex", "urn:ex/")


class AirFlowStation(Device):
    airInlet: AirInlet
    airOutlet: AirOutlet
    flow = AnalogIn


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


class VAV(System):
    hotDeckAirInlet: AirInlet
    coldDeckAirInlet: AirInlet
    supplyAirOutlet: AirOutlet
    hotDeckAirFlow: AnalogIn
    coldDeckAirFlow: AnalogIn
    hotDeckDamperPosition: AnalogOut
    coldDeckDamperPosition: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a hot deck air flow station
        self.hot_deck_air_flow_station = AirFlowStation(
            label=self.label + ".hot_deck_air_flow_station"
        )
        self > self.hot_deck_air_flow_station
        self.hotDeckAirInlet >> self.hot_deck_air_flow_station.airInlet
        self.hotDeckAirFlow = self.hot_deck_air_flow_station.flow

        # create a hot deck damper
        self.hot_deck_damper = Damper(label=self.label + ".hot_deck_damper")
        self > self.hot_deck_damper
        self.hot_deck_air_flow_station >> self.hot_deck_damper
        self.hotDeckDamperPosition = self.hot_deck_damper.position

        # create a cold deck air flow station
        self.cold_deck_air_flow_station = AirFlowStation(
            label=self.label + ".cold_deck_air_flow_station"
        )
        self > self.cold_deck_air_flow_station
        self.coldDeckAirInlet >> self.cold_deck_air_flow_station.airInlet
        self.coldDeckAirFlow = self.cold_deck_air_flow_station.flow

        # create a cold deck damper
        self.cold_deck_damper = Damper(label=self.label + ".cold_deck_damper")
        self > self.cold_deck_damper
        self.cold_deck_air_flow_station >> self.cold_deck_damper
        self.coldDeckDamperPosition = self.cold_deck_damper.position

        # connection for merge
        merged_air = AirConnection(label=self.label + ".merge")

        # link the air pieces together
        self.hot_deck_damper.airOutlet >> merged_air
        self.cold_deck_damper.airOutlet >> merged_air
        merged_air >> self.supplyAirOutlet


# make one
vav = VAV(label="A-7")

g36_header("figure007")
dump()
