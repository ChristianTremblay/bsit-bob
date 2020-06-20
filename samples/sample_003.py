from bob import dump
from bob.air import Fan, Zone
from bob.cw import ChilledWaterConnection, ChilledWaterCoil

# there is a chilled water connection, we don't know where the chilled
# is coming from
c = ChilledWaterConnection()

# there is a chilled water coil (itself a system) that is a subsystem
# of a larger context
coil1 = ChilledWaterCoil(label="CW-Coil-1")

# the coil gets its chilled water from the connection
c >> coil1

# there is a fan, and the air output of the fan goes into the coil
f = Fan(label="F")
f >> coil1

# there is a zone, and the air output of the coil is goes into the zone
z = Zone(label="Zone-1")
coil1 >> z

# dump the result
if __name__ == "__main__":
    dump()
