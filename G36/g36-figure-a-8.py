"""
Figure A-8
"""

from __future__ import annotations

from typing import Any
from pathlib import Path

from bob.core import bind_model_namespace, Device, System, dump
from bob.connections.air import (
    AirConnection,
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from bob.signal import AnalogIn, AnalogOut

from header import g36_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace(
    "exg3608", f"http://data.ashrae.org/standard223/data/{model_name}#"
)


class AirFlowStation(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    flow = AnalogIn


class DamperPositioner(Device):
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
        self.hotDeckAirInlet.mapsTo = self.hot_deck_damper.airInlet
        self.hotDeckDamperPosition = self.hot_deck_damper.position

        # create a cold deck damper
        self.cold_deck_damper = Damper(label=self.label + ".cold_deck_damper")
        self > self.cold_deck_damper
        self.coldDeckAirInlet.mapsTo = self.cold_deck_damper.airInlet
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
        self.supplyAirOutlet.mapsTo = self.air_flow_station.airOutlet


# make one
vav = VAV(label="A-8")

g36_header(model_name)
dump()
