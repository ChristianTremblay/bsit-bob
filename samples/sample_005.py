from bob import dump
from bob.air import AirConnection, Zone
from bob.vav import VAV2

# create Zone-1 and its VAV connected together
zone1 = Zone(name="Zone-1")
vav1 = VAV2(name="Zone-1.VAV")
vav1 >> zone1

# create Zone-2 and its VAV connected together
zone2 = Zone(name="Zone-2")
vav2 = VAV2(name="Zone-2.VAV")
vav2 >> zone2

# common supply connection shared
supply_air = AirConnection(name="SupplyAir")
supply_air >> vav1
supply_air >> vav2

# similar for return air
return_air = AirConnection(name="ReturnAir")
zone1 >> return_air
zone2 >> return_air

# dump the result
if __name__ == "__main__":
    dump()
