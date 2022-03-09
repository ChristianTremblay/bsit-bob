"""
Dual Duct AHU
"""

from __future__ import annotations

from typing import Any
from pathlib import Path

from bob.core import bind_model_namespace, Junction, System, dump
from bob.connections.air import (
    AirConnection,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from bob.devices.hvac.damper import Damper
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.filter import Filter

from bob.sensor.pressure import DifferentialStaticPressureSensor
#not sure of the difference between differential pressure and differential static pressure in this case

from bob.systems.archives.coolingcoil import ChilledWaterCoil2
from bob.systems.archives.heatingcoil import HotWaterCoil2

from header import lbnl_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace(
    "exFDD", f"http://data.ashrae.org/standard223/data/{model_name}#"
)

class HotDeck(System):
    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        in_filter = Filter(label = self.label + '.filter')
        self.airInlet.mapsTo = in_filter.airInlet
        hwc = HotWaterCoil2(label = self.label + '.hot_water_coil')
        hsf = Fan(label = self.label + '.hot_supply_fan')
        self.airOutlet.mapsTo = hsf.airOutlet
        in_filter >> hwc >> hsf

        hsf_dp = DifferentialStaticPressureSensor(label = self.label + '.hot_supply_fan_dp_sensor')
        hsf_dp.hasMeasurementLocationHigh = hsf.airOutlet
        hsf_dp.hasMeasurementLocationLow = hsf.airInlet
        #more sensors



class DDAHU(System):
    outsideAirInlet: AirInletSystemConnectionPoint
    returnAirInlet: AirInletSystemConnectionPoint
    supplyHotAirOutlet: AirOutletSystemConnectionPoint
    supplyColdAirOutlet: AirOutletSystemConnectionPoint
    exhaustAirOutlet: AirOutletSystemConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        oa_damper = Damper(label=self.label + ".min_oa_damper") 

        self.outsideAirInlet.mapsTo = oa_damper.airInlet
        #sensors attach here

        mixed_air = AirConnection(label=self.label + ".mixed_air")
        oa_damper >> mixed_air

        return_air_fan = Fan(label = self.label + ".return_air_fan")
        self.returnAirInlet.mapsTo = return_air_fan.airInlet
        #sensors here and about fan

        j1 = Junction()
        j1.link_to(return_air_fan.airOutlet)

        recirc_damper = Damper(label = self.label + ".recirculated_air_damper")
        exhaust_damper = Damper(label = self.label + ".exhaust_damper")

        j1.link_to(recirc_damper.airInlet)
        j1.link_to(exhaust_damper.airInlet)

        self.exhaustAirOutlet.mapsTo = exhaust_damper.airOutlet

        recirc_damper >> mixed_air

        hot_deck = HotDeck(label = self.label + 'hot_deck')
        mixed_air >> hot_deck.airInlet

# make one
ddahu = DDAHU(label="DDAHU")

lbnl_header(model_name)
dump()
