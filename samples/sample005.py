from pathlib import Path

from bob.core import bind_model_namespace, data_graph, schema_graph, dump
from bob.scratch.header import sample_header

from bob.core import PhysicalSpace
from bob.connections.air import AirConnection
from bob.equipment.hvac.vav import VAV
from bob.space.hvac import HVACSpace, HVACZone

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# create Zone-1 and its VAV connected together
zone1 = HVACZone(label="Zone-1")

hvacspace1 = HVACSpace(label="Space-1")
hvacspace2 = HVACSpace(label="Space-2")
zone1 > [hvacspace1, hvacspace2]

# there is a room that contains both spaces
room1 = PhysicalSpace(label="Room 191")
room1 > [hvacspace1, hvacspace2]

# make a VAV terminal unit
vav1 = VAV(label="Zone-1.VAV")
vav1.serves = zone1
vav1.airOutlet >> hvacspace1.ductAirInlet

# No ZN-T in the Bob version
# vav1["ZN-T"].hasObservationLocation = hvacspace1

# create Zone-2 and its VAV connected together
vav2 = VAV(label="Zone-2.VAV")
vav2.serves = zone1

# No ZN-T in the Bob version
# vav2["ZN-T"].hasObservationLocation = hvacspace2

# common supply connection shared
supply_air = AirConnection(label="SupplyAir")
supply_air >> vav1
supply_air >> vav2

# similar for return air
return_air = AirConnection(label="ReturnAir")
hvacspace1.ductAirOutlet >> return_air
hvacspace2.ductAirOutlet >> return_air

# dump the result
dump(
    data_graph,
    filename=f"samples/ttl/{model_name}.data.ttl",
    header=sample_header(model_name),
)
dump(schema_graph, filename=f"samples/ttl/{model_name}.schema.ttl")
