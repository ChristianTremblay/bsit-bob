from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.core import Equipment, bind_model_namespace, data_graph, dump, schema_graph
from bob.scratch.header import sample_header

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

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
