import sys
from typing import Any

from bob.core import bind_model_namespace, System, Device, dump
from bob.air import (
    AirConnection,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    Damper,
    Fan,
    Filter,
    AirFlowStation,
    Zone,
)
from bob.cw import ChilledWaterCoil2
from bob.hw import HotWaterConnection, HotWaterBoiler, HotWaterCoil2
from bob.vav import VAV2


__namespace__ = bind_model_namespace("ex", "urn:ex/")


class OutsideAirSupply(System):
    airOutlet: AirOutletConnectionPoint


class OutsideAirExhaust(System):
    airInlet: AirInletConnectionPoint


class AHU(System):
    outsideAirInlet: AirInletConnectionPoint
    supplyAirOutlet: AirOutletConnectionPoint
    returnAirInlet: AirInletConnectionPoint
    exhaustAirOutlet: AirOutletConnectionPoint

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

        self.hot_water_coil = HotWaterCoil2(label=self.label + ".hot_water_coil")
        mixed_air_filter >> self.hot_water_coil

        self.chilled_water_coil = ChilledWaterCoil2(
            label=self.label + ".chilled_water_coil"
        )
        self.hot_water_coil >> self.chilled_water_coil

        supply_fan = Fan(label=self.label + ".supply_fan")
        self.chilled_water_coil >> supply_fan

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


# create the air handler
ahu = AHU(label="ahu_1")

# connect to outside air instances
outside_air_supply = OutsideAirSupply(label="outside_air_supply")
outside_air_supply.airOutlet >> ahu.outsideAirInlet

outside_air_exhaust = OutsideAirExhaust(label="outside_air_exhaust")
ahu.exhaustAirOutlet >> outside_air_exhaust.airInlet

# create Zone-1 and its VAV connected together
zone_1 = Zone(label="zone_1")
vav_1 = VAV2(label="vav_1")
vav_1 >> zone_1

# create Zone-2 and its VAV connected together
zone_2 = Zone(label="zone_2")
vav_2 = VAV2(label="vav_2")
vav_2 >> zone_2

# common supply connection shared
supply_air = AirConnection(label="supply_air")
ahu.supplyAirOutlet >> supply_air
supply_air >> vav_1.airInlet
supply_air >> vav_2.airInlet

# similar for return air
return_air = AirConnection(label="return_air")
zone_1.returnAirOutlet >> return_air
zone_2.returnAirOutlet >> return_air
return_air >> ahu.returnAirInlet

# create a hot water system with a boiler
hw_sys = System(label="hw_sys")
boiler_1 = HotWaterBoiler(label="boiler_1")

# add the components to the system
hw_sys > boiler_1
hw_sys > ahu.hot_water_coil
hw_sys > vav_1.hot_water_coil
hw_sys > vav_2.hot_water_coil

# hot water supply side
hw_sys_supply = HotWaterConnection(label="hw_sys.supply")
boiler_1 >> hw_sys_supply
hw_sys_supply >> ahu.hot_water_coil.hot_water_valve.hotWaterInlet
hw_sys_supply >> vav_1.hot_water_valve.hotWaterInlet
hw_sys_supply >> vav_2.hot_water_valve.hotWaterInlet

# hot water return side
hw_sys_return = HotWaterConnection(label="hw_sys.return")
ahu.hot_water_coil >> hw_sys_return
vav_1.hot_water_coil >> hw_sys_return
vav_2.hot_water_coil >> hw_sys_return
hw_sys_return >> boiler_1

# dump the result
if __name__ == "__main__":
    dump()
