"""
Figure A-9
"""

from __future__ import annotations

from typing import Any

from bob.core import bind_model_namespace, System, Device, dump
from bob.air import (
    AirConnection,
    AirInlet,
    AirOutlet,
    Damper,
    Fan,
    Filter,
    AirFlowStation,
    Zone,
)
from bob.cw import ChilledWaterCoil2
from bob.hw import HotWaterCoil2

from header import g36_header


__namespace__ = bind_model_namespace("ex", "urn:ex/")


class AHU(System):
    outsideAirInlet: AirInlet
    supplyAirOutlet: AirOutlet
    returnAirInlet: AirInlet
    exhaustAirOutlet: AirOutlet

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        outside_air = AirConnection(label=self.label + ".outside_air")
        self.outsideAirInlet >> outside_air

        min_oa_damper = Damper(label=self.label + ".min_oa_damper")
        outside_air >> min_oa_damper.airInlet

        outside_air_afms = AirFlowStation(label=self.label + ".outside_air_afms")
        min_oa_damper >> outside_air_afms

        economizer_oa_damper = Damper(label=self.label + ".economizer_oa_damper")
        outside_air >> economizer_oa_damper.airInlet

        mixed_air = AirConnection(label=self.label + ".mixed_air")
        outside_air_afms >> mixed_air
        economizer_oa_damper >> mixed_air

        mixed_air_filter = Filter(label=self.label + ".mixed_air_filter")
        mixed_air >> mixed_air_filter.airInlet

        hot_water_coil = HotWaterCoil2(label=self.label + ".hot_water_coil")
        mixed_air_filter >> hot_water_coil

        chilled_water_coil = ChilledWaterCoil2(label=self.label + ".chilled_water_coil")
        hot_water_coil >> chilled_water_coil

        supply_fan = Fan(label=self.label + ".supply_fan")
        chilled_water_coil >> supply_fan

        return_fan = Fan(label=self.label + ".return_fan")
        self.returnAirInlet >> return_fan.airInlet

        # return air goes to two dampers
        return_air = AirConnection(label=self.label + ".return_air")

        # make the exhaust air damper and connect it
        exhaust_air_damper = Damper(label=self.label + ".exhaust_air_damper")
        return_air >> exhaust_air_damper
        exhaust_air_damper.airOutlet >> self.exhaustAirOutlet

        # the return air damper gets its input from the return fan and goes to
        # into the mixed air
        return_air_damper = Damper(label=self.label + ".return_air_damper")
        return_air >> return_air_damper >> mixed_air


# make one
ahu = AHU(label="A-9")

g36_header("figure009")
dump()
