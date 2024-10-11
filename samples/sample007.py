from pathlib import Path

from bob.core import bind_model_namespace, data_graph, schema_graph, dump
from bob.scratch.header import sample_header

from bob.core import Equipment

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class TestEquipment(Equipment):
    pass


class Part1(Equipment):
    pass


class Part2(Equipment):
    pass


# Equipment has two parts
d1 = TestEquipment(label="Test Equipment 1")
p11 = Part1(label="p11")
p12 = Part2(label="p12")

d1 > p11
d1 > p12

# Equipment has a part p1 which has a part p2
d2 = TestEquipment(label="Test Equipment 2")
p21 = Part1(label="p21")
p22 = Part2(label="p22")

d2 > p21 > p22

# p1 is a part of p2 which is a part of a Equipment
d3 = TestEquipment(label="Test Equipment 3")
p31 = Part1(label="p31")
p32 = Part2(label="p32")

p31 < p32 < d3

# dump the result
dump(
    data_graph,
    filename=f"samples/ttl/{model_name}.data.ttl",
    header=sample_header(model_name),
)
dump(schema_graph, filename=f"samples/ttl/{model_name}.schema.ttl")
