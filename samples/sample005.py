from pathlib import Path

from header import sample_header

from bob.connections.air import AirConnection
from bob.core import bind_model_namespace, dump
from bob.equipment.hvac.vav import VAV_Simple
from bob.space.hvac import HVACSpace, HVACZone

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# create Zone-1 and its VAV connected together
zone1 = HVACZone(label="Zone-1")

hvacspace1 = HVACSpace(label="Space-1")
hvacspace2 = HVACSpace(label="Space-2")

zone1 > [hvacspace1, hvacspace2]

vav1 = VAV_Simple(label="Zone-1.VAV")
vav1.serves = zone1
vav1.airOutlet >> hvacspace1.ductAirInlet

# create Zone-2 and its VAV connected together
vav2 = VAV_Simple(label="Zone-2.VAV")
vav2.serves = zone1

# common supply connection shared
supply_air = AirConnection(label="SupplyAir")
supply_air >> vav1
supply_air >> vav2

# similar for return air
return_air = AirConnection(label="ReturnAir")
hvacspace1.ductAirOutlet >> return_air
hvacspace2.ductAirOutlet >> return_air

# dump the result
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
