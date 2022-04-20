"""
Figure A-10
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from header import g36_header

from bob.connections.air import (
    AirConnection,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from bob.connections.electricity import ElectricalInletConnectionPoint
from bob.core import Junction, System, bind_model_namespace, dump
from bob.devices.hvac.damper import Damper
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.filter import Filter
from bob.systems.archives.coolingcoil import ChilledWaterCoil2
from bob.systems.archives.heatingcoil import HotWaterCoil2

model_name = Path(__file__).stem
_namespace = bind_model_namespace(
    "exg3610", f"http://data.ashrae.org/standard223/data/{model_name}#"
)


class AHU(System):
    outsideAirInlet: AirInletSystemConnectionPoint
    supplyAirOutlet: AirOutletSystemConnectionPoint
    returnAirInlet: AirInletSystemConnectionPoint
    exhaustAirOutlet: AirOutletSystemConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        min_oa_damper = Damper(label=self.label + ".min_oa_damper")
        economizer_oa_damper = Damper(label=self.label + ".economizer_oa_damper")

        # outside air inlet goes to both dampers
        junction = Junction()
        junction >> min_oa_damper.airInlet
        junction >> economizer_oa_damper.airInlet
        self.outsideAirInlet.mapsTo = junction

        mixed_air = AirConnection(label=self.label + ".mixed_air")
        min_oa_damper >> mixed_air
        economizer_oa_damper >> mixed_air

        mixed_air_filter = Filter(label=self.label + ".mixed_air_filter")
        mixed_air >> mixed_air_filter.airInlet

        hot_water_coil = HotWaterCoil2(label=self.label + ".hot_water_coil")
        mixed_air_filter >> hot_water_coil

        chilled_water_coil = ChilledWaterCoil2(label=self.label + ".chilled_water_coil")
        hot_water_coil >> chilled_water_coil

        supply_fan = Fan(
            label=self.label + ".supply_fan",
            electricalInlet=ElectricalInletConnectionPoint,
        )
        chilled_water_coil >> supply_fan

        # suuply air outlet goes to a segment with a temperature sensor then to
        # the system connection point
        junction = Junction()
        junction >> supply_fan.airOutlet
        self.supplyAirOutlet.mapsTo = junction

        relief_fan = Fan(
            label=self.label + ".relief_fan",
            electricalInlet=ElectricalInletConnectionPoint,
        )
        return_air_damper = Damper(label=self.label + ".return_air_damper")

        # return air inlet goes to a segment with a temperature sensor then to
        # the relief fan and return air damper
        j1 = Junction()
        j2 = Junction()

        j1.link_to(j2)
        j2.link_to(relief_fan.airInlet)
        j2.link_to(return_air_damper.airInlet)
        self.returnAirInlet.mapsTo = j1

        # output of the return air damper is mixed air
        return_air_damper >> mixed_air

        # make the relief air damper and connect it
        relief_air_damper = Damper(label=self.label + ".relief_air_damper")
        relief_fan >> relief_air_damper

        self.exhaustAirOutlet.mapsTo = relief_air_damper.airOutlet


# make one
ahu = AHU(label="A-10")

dump(filename=f"G36/ttl/{model_name}.ttl", header=g36_header(model_name))
