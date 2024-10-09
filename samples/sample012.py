from pathlib import Path

from bob.core import bind_model_namespace, data_graph, schema_graph, dump
from bob.scratch.header import sample_header

from bob.core import (
    Equipment,
    System,
    BoundaryConnectionPoint,
)
from bob.connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class TestSystem(System):
    cpIn: BoundaryConnectionPoint
    cpOut: BoundaryConnectionPoint


class TestEquipment(Equipment):
    cpIn: AirInletConnectionPoint
    cpOut: AirOutletConnectionPoint


# make a system and a Equipment
s1 = TestSystem(label="s1")
d1 = TestEquipment(label="d1")
d1 < s1

# make a system and a Equipment
s2 = TestSystem(label="s2")
d2 = TestEquipment(label="d2")
d2 < s2

# pass-in from the system to the Equipment
s2.cpIn = d2.cpIn

# pass-out from the Equipment to the system
s2.cpOut = d2.cpOut

# dump the result
dump(
    data_graph,
    filename=f"samples/ttl/{model_name}.data.ttl",
    header=sample_header(model_name),
)
dump(schema_graph, filename=f"samples/ttl/{model_name}.schema.ttl")
