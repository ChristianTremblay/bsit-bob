"""
Figure A-5
"""

from __future__ import annotations

from typing import Any
from pathlib import Path

from bob.core import bind_model_namespace, Junction, Device, System, dump
from bob.connections.air import (
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from bob.connections.water import (
    HotWaterInletConnectionPoint,
    HotWaterInletSystemConnectionPoint,
    HotWaterOutletConnectionPoint,
    HotWaterOutletSystemConnectionPoint,
)
from bob.devices.hvac.fan import Fan
from bob.signal import AnalogIn, AnalogOut

from header import g36_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace(
    "exg3605", f"http://data.ashrae.org/standard223/data/{model_name}#"
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


class ValvePositioner(Device):
    position = AnalogOut


class HotWaterValve(Device):
    pass


class HotWaterCoil(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    hwInlet: HotWaterInletConnectionPoint
    hwOutlet: HotWaterOutletConnectionPoint
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
    hwInlet: HotWaterInletSystemConnectionPoint
    hwOutlet: HotWaterOutletSystemConnectionPoint
    hwValvePosition: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create an air flow station
        self.air_flow_station = AirFlowStation(label=self.label + ".air_flow_station")
        self > self.air_flow_station
        self.supplyAirInlet.mapsTo = self.air_flow_station.airInlet
        self.supplyAirFlow = self.air_flow_station.flow

        # create a damper
        self.damper = Damper(label=self.label + ".damper")
        self > self.damper
        self.damperPosition = self.damper.position

        # create a fan
        self.fan = Fan(label=self.label + ".fan")
        self > self.fan

        # create a hot water coil
        self.hot_water_coil = HotWaterCoil(label=self.label + ".hot_water_coil")
        self > self.hot_water_coil
        self.hwInlet.mapsTo = self.hot_water_coil.hwInlet
        self.hwOutlet.mapsTo = self.hot_water_coil.hwOutlet
        self.hwValvePosition = self.hot_water_coil.valvePosition

        # fan output goes to the hot water coil
        self.fan >> self.hot_water_coil
        self.supplyAirOutlet.mapsTo = self.hot_water_coil.airOutlet

        # merge the inlets together
        junction = Junction()
        junction.link_to(self.damper.airOutlet)
        junction.link_to(self.fan.airInlet)
        self.returnAirInlet.mapsTo = junction


# make one
vav = VAV(label="A-5")

g36_header(model_name)
dump()
