"""
Figure A-9
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from header import g36_header

from bob.connections.air import (
    AirConnection,
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from bob.connections.electricity import ElectricalInletConnectionPoint
from bob.core import Device, Junction, System, bind_model_namespace, dump
from bob.devices.hvac.fan import Fan
from bob.signal import AnalogIn, AnalogOut
from bob.systems.archives.coolingcoil import ChilledWaterCoil2
from bob.systems.archives.heatingcoil import HotWaterCoil2

model_name = Path(__file__).stem
_namespace = bind_model_namespace(
    "exg3609", f"http://data.ashrae.org/standard223/data/{model_name}#"
)


class AirFilter(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    dp = AnalogIn


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


class AHU(System):
    outsideAirInlet: AirInletSystemConnectionPoint
    supplyAirOutlet: AirOutletSystemConnectionPoint
    returnAirInlet: AirInletSystemConnectionPoint
    exhaustAirOutlet: AirOutletSystemConnectionPoint

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        _electricalInlet = kwargs.pop("electricalInlet")

        super().__init__(config, **kwargs)

        min_oa_damper = Damper(label=self.label + ".min_oa_damper")
        economizer_oa_damper = Damper(label=self.label + ".economizer_oa_damper")

        # merge the inlets together
        junction = Junction()
        junction.link_to(min_oa_damper.airInlet)
        junction.link_to(economizer_oa_damper.airInlet)
        self.outsideAirInlet.mapsTo = junction

        outside_air_afms = AirFlowStation(label=self.label + ".outside_air_afms")
        min_oa_damper >> outside_air_afms

        mixed_air = AirConnection(label=self.label + ".mixed_air")
        outside_air_afms >> mixed_air
        economizer_oa_damper >> mixed_air

        mixed_air_filter = AirFilter(label=self.label + ".mixed_air_filter")
        mixed_air >> mixed_air_filter.airInlet

        hot_water_coil = HotWaterCoil2(label=self.label + ".hot_water_coil")
        mixed_air_filter >> hot_water_coil

        chilled_water_coil = ChilledWaterCoil2(label=self.label + ".chilled_water_coil")
        hot_water_coil >> chilled_water_coil

        supply_fan = Fan(
            label=self.label + ".supply_fan", electricalInlet=_electricalInlet
        )
        chilled_water_coil >> supply_fan
        self.supplyAirOutlet.mapsTo = supply_fan.airOutlet

        return_fan = Fan(
            label=self.label + ".return_fan", electricalInlet=_electricalInlet
        )
        self.returnAirInlet.mapsTo = return_fan.airInlet

        # return air goes to two dampers
        return_air = AirConnection(label=self.label + ".return_air")

        # make the exhaust air damper and connect it
        exhaust_air_damper = Damper(label=self.label + ".exhaust_air_damper")
        return_air >> exhaust_air_damper
        self.exhaustAirOutlet.mapsTo = exhaust_air_damper.airOutlet

        # the return air damper gets its input from the return fan and goes to
        # into the mixed air
        return_air_damper = Damper(label=self.label + ".return_air_damper")
        return_air >> return_air_damper >> mixed_air


# make one
ahu = AHU(label="A-9", electricalInlet=ElectricalInletConnectionPoint)

dump(filename=f"G36/ttl/{model_name}.ttl", header=g36_header(model_name))
