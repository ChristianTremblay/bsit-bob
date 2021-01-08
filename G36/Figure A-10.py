"""
Figure A-10
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

        economizer_oa_damper = Damper(label=self.label + ".economizer_oa_damper")
        outside_air >> economizer_oa_damper.airInlet

        mixed_air = AirConnection(label=self.label + ".mixed_air")
        min_oa_damper >> mixed_air
        economizer_oa_damper >> mixed_air

        mixed_air_filter = Filter(label=self.label + ".mixed_air_filter")
        mixed_air >> mixed_air_filter.airInlet

        hot_water_coil = HotWaterCoil2(label=self.label + ".hot_water_coil")
        mixed_air_filter >> hot_water_coil

        chilled_water_coil = ChilledWaterCoil2(label=self.label + ".chilled_water_coil")
        hot_water_coil >> chilled_water_coil

        supply_fan = Fan(label=self.label + ".supply_fan")
        chilled_water_coil >> supply_fan

        # return air goes to the mixed air damper or the fan
        return_air = AirConnection(label=self.label + ".return_air")
        self.returnAirInlet >> return_air

        return_fan = Fan(label=self.label + ".return_fan")
        return_air >> return_fan

        mixed_air_damper = Damper(label=self.label + ".mixed_air_damper")
        return_air >> mixed_air_damper >> mixed_air

        # make the relief air damper and connect it
        relief_air_damper = Damper(label=self.label + ".relief_air_damper")
        return_fan >> relief_air_damper
        relief_air_damper.airOutlet >> self.exhaustAirOutlet

# make one
ahu = AHU(label="A-10")

g36_header("figure010")
dump()
