"""
Figure A-7
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from header import g36_header

from bob.connections.air import (
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from bob.core import Device, Junction, System, bind_model_namespace, dump
from bob.signal import AnalogIn, AnalogOut

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace(
    "exg3607", f"http://data.ashrae.org/standard223/data/{model_name}#"
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
        self.hotDeckAirInlet.mapsTo = self.hot_deck_air_flow_station.airInlet
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
        self.coldDeckAirInlet.mapsTo = self.cold_deck_air_flow_station.airInlet
        self.coldDeckAirFlow = self.cold_deck_air_flow_station.flow

        # create a cold deck damper
        self.cold_deck_damper = Damper(label=self.label + ".cold_deck_damper")
        self > self.cold_deck_damper
        self.cold_deck_air_flow_station >> self.cold_deck_damper
        self.coldDeckDamperPosition = self.cold_deck_damper.position

        # merge the outlets together
        junction = Junction()
        junction.link_to(self.hot_deck_damper.airOutlet)
        junction.link_to(self.cold_deck_damper.airOutlet)
        self.supplyAirOutlet.mapsTo = junction


# make one
vav = VAV(label="A-7")

dump(filename=f"G36/ttl/{model_name}.ttl", header=g36_header(model_name))
