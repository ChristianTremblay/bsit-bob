"""
Figure A-8
"""

from __future__ import annotations

from typing import Any

from bob import bind_model_namespace, dump

from bob.core import System, Device, Part
from bob.air import (
    AirConnection,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
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


class VAV(System):
    hotDeckAirInlet: AirInletSystemConnectionPoint
    coldDeckAirInlet: AirInletSystemConnectionPoint
    supplyAirOutlet: AirOutletSystemConnectionPoint
    supplyAirFlow: AnalogIn
    hotDeckDamperPosition: AnalogOut
    coldDeckDamperPosition: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a hot deck damper
        self.hot_deck_damper = Damper(label=self.label + ".hot_deck_damper")
        self > self.hot_deck_damper
        self.hotDeckAirInlet > self.hot_deck_damper.airInlet
        self.hotDeckDamperPosition = self.hot_deck_damper.position

        # create a cold deck damper
        self.cold_deck_damper = Damper(label=self.label + ".cold_deck_damper")
        self > self.cold_deck_damper
        self.coldDeckAirInlet > self.cold_deck_damper.airInlet
        self.coldDeckDamperPosition = self.cold_deck_damper.position

        # create an air flow station
        self.air_flow_station = AirFlowStation(label=self.label + ".air_flow_station")
        self > self.air_flow_station
        self.supplyAirFlow = self.air_flow_station.flow

        # connection for merge
        merged_air = AirConnection(label=self.label + ".merge")

        # link the air pieces together
        self.hot_deck_damper.airOutlet >> merged_air
        self.cold_deck_damper.airOutlet >> merged_air
        merged_air >> self.air_flow_station.airInlet

        # supply air outlet comes from the air flow station
        self.supplyAirOutlet > self.air_flow_station.airOutlet


# make one
vav = VAV(label="A-8")

g36_header("figure008")
dump()
