"""
Figure A-10
"""

from __future__ import annotations

from typing import Any

from bob.core import bind_model_namespace, System, Device, dump
from bob.air import (
    AirConnection,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
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
    outsideAirInlet: AirInletSystemConnectionPoint
    supplyAirOutlet: AirOutletSystemConnectionPoint
    returnAirInlet: AirInletSystemConnectionPoint
    exhaustAirOutlet: AirOutletSystemConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        min_oa_damper = Damper(label=self.label + ".min_oa_damper")
        self.outsideAirInlet > min_oa_damper.airInlet

        economizer_oa_damper = Damper(label=self.label + ".economizer_oa_damper")
        self.outsideAirInlet > economizer_oa_damper.airInlet

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

        relief_fan = Fan(label=self.label + ".relief_fan")
        self.returnAirInlet > relief_fan.airInlet

        mixed_air_damper = Damper(label=self.label + ".mixed_air_damper")
        self.returnAirInlet > mixed_air_damper.airInlet

        # output of the damper is mixed air
        mixed_air_damper >> mixed_air

        # make the relief air damper and connect it
        relief_air_damper = Damper(label=self.label + ".relief_air_damper")
        relief_fan >> relief_air_damper

        self.exhaustAirOutlet > relief_air_damper.airOutlet

# make one
ahu = AHU(label="A-10")

g36_header("figure010")
dump()
