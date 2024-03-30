from pathlib import Path

from header import sample_header

from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.core import (
    Equipment,
    Junction,
    bind_model_namespace,
    data_graph,
    dump,
    schema_graph,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class Thing1(Equipment):
    ocp: AirOutletConnectionPoint


equip1 = Thing1(label="equip1")

#


class Thing2(Equipment):
    icp: AirInletConnectionPoint


equip2 = Thing2(label="equip2")

#


class ChildThing1(Equipment):
    ocp: AirOutletConnectionPoint


equip1a = ChildThing1(label="equip1a")
equip1b = ChildThing1(label="equip1b")

# contains
equip1 > [equip1a, equip1b]

# equip1 also contains a junction (should be checked/asserted by maps_to)
j = Junction()
equip1 > j

equip1a >> j
equip1b.ocp >> j

j.maps_to(equip1.ocp)

#

equip1 >> equip2

# dump the result
dump(
    data_graph,
    filename=f"samples/ttl/{model_name}.data.ttl",
    header=sample_header(model_name),
)
dump(schema_graph, filename=f"samples/ttl/{model_name}.schema.ttl")
