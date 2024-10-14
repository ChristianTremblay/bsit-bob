from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.core import (
    BoundaryConnectionPoint,
    Equipment,
    InletConnectionPoint,
    OutletConnectionPoint,
    System,
    bind_model_namespace,
    data_graph,
    dump,
    schema_graph,
)
from bob.scratch.header import sample_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class TestSystem(System):
    cpIn: BoundaryConnectionPoint
    cpOut: BoundaryConnectionPoint


class TestEquipment(Equipment):
    cpIn: InletConnectionPoint
    cpOut: OutletConnectionPoint


# make a system and a piece of equipment
s1 = TestSystem(label="s1")
d1 = TestEquipment(label="d1")
d1 < s1

# pass through the system connection points
# s1.cpIn >> s1.cpOut

# make a system and a Equipment
s2 = TestSystem(label="s2")
d2 = TestEquipment(label="d2")
d2 < s2

# pass-in from the system to the Equipment
s2.cpIn = d2.cpIn

# pass-out from the Equipment to the system
s2.cpOut = d2.cpOut

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
