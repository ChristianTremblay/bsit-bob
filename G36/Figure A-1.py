"""
Figure A-1
"""

from __future__ import annotations

from typing import Any

from bob import bind_model_namespace, dump

from bob.core import System, Device, Part
from bob.air import AirInlet, AirOutlet
from bob.signal import AnalogIn, AnalogOut

from header import g36_header

__namespace__ = bind_model_namespace("ex", "urn:ex/")


class AirFlowStation(Device):
    airInlet: AirInlet
    airOutlet: AirOutlet
    flow = AnalogIn

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
    airInlet: AirInlet
    airOutlet: AirOutlet
    airFlow: AnalogIn
    damperPosition: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create an air flow station
        self.air_flow_station = AirFlowStation(label=self.label + ".air_flow_station")
        self > self.air_flow_station

        # create a damper
        self.damper = Damper(label=self.label + ".damper")
        self > self.damper

        # link the air pieces together
        self.air_flow_station >> self.damper

        # reference the connections
        self.airInlet >> self.air_flow_station.airInlet
        self.airOutlet << self.damper.airOutlet
        self.airFlow = self.air_flow_station.flow
        self.damperPosition = self.damper.position


# make one
vav = VAV(label="A-1")

g36_header("figure001")
dump()
