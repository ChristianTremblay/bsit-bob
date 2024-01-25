from pathlib import Path

from bob.core import bind_model_namespace, data_graph, schema_graph, dump
from header import sample_header

from bob.core import Equipment, Junction
from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class Thing0(Equipment):
    ocp: AirOutletConnectionPoint

equip0 = Thing0(label="equip0")

class Thing1(Equipment):
    icp: AirInletConnectionPoint

equip1 = Thing1(label="equip1")

class ChildThing1(Equipment):
    icp: AirInletConnectionPoint

equip1a = ChildThing1(label="equip1a")
equip1b = ChildThing1(label="equip1b")

# contains
equip1 > [equip1a, equip1b]

# equip1 also contains a junction (should be checked/asserted by maps_to)
j = Junction()
equip1 > j

j >> equip1a
j >> equip1b.icp

j.maps_to(equip1.icp)

#

equip0 >> equip1

# dump the result
dump(
    data_graph,
    filename=f"samples/ttl/{model_name}.data.ttl",
    header=sample_header(model_name),
)
dump(schema_graph, filename=f"samples/ttl/{model_name}.schema.ttl")
