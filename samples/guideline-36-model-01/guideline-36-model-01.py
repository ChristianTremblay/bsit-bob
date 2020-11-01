from bob.core import bind_model_namespace, Device, dump
from bob.air import AirConnection, AirInlet, AirOutlet, Damper, Fan, AirFlowStation, Zone
from bob.cw import ChilledWaterCoil2
from bob.hw import HotWaterCoil2
from bob.vav import VAV2


__namespace__ = bind_model_namespace("ex", "urn:ex/")


class OutsideAir(Device):
    oa: AirOutlet  # outside air goes in someplace
    econ: AirOutlet  # outside air going into the economizer
    ea: AirInlet  # from exhaust fan going out


# start with outside air
outside_air = OutsideAir(label="outside_air")

min_oa_damper = Damper(label="min_oa_damper")
outside_air.oa >> min_oa_damper.ain

outside_air_afms = AirFlowStation(label="outside_air_afms")
min_oa_damper >> outside_air_afms

economizer_oa_damper = Damper(label="economizer_oa_damper")
outside_air.econ >> economizer_oa_damper.ain

mixed_air = AirConnection(label="mixed_air")
outside_air_afms.aout >> mixed_air
economizer_oa_damper.aout >> mixed_air

mixed_air_damper = Damper(label="mixed_air_damper")
mixed_air_damper.ain << mixed_air

hot_water_coil = HotWaterCoil2(label="hot_water_coil")
mixed_air_damper >> hot_water_coil

chilled_water_coil = ChilledWaterCoil2(label="chilled_water_coil")
hot_water_coil >> chilled_water_coil

supply_fan = Fan(label="supply_fan")
chilled_water_coil >> supply_fan

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
supply_air >> vav_1
supply_air >> vav_2

# similar for return air
return_air = AirConnection(label="return_air")
zone_1 >> return_air
zone_2 >> return_air

# start with the return fan
return_fan = Fan(label="return_fan")

# connect the supply air and return air connections
supply_fan >> supply_air
return_air >> return_fan

# make the exhaust air damper and connect it
exhaust_air_damper = Damper(label="exhaust_air_damper")
return_fan >> exhaust_air_damper
exhaust_air_damper.aout >> outside_air.ea

# the return air damper gets its input from the return fan and goes to
# into the mixed air
return_air_damper = Damper(label="return_air_damper")
return_fan.aout.connectedThrough >> return_air_damper  # type: ignore[operator]
return_air_damper.aout >> mixed_air

# dump the result
if __name__ == "__main__":
    dump()
