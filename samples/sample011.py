from pathlib import Path

from header import sample_header

from bob.core import (
    Equipment,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    System,
    bind_model_namespace,
    dump,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class TestSystem(System):
    cpIn: InletSystemConnectionPoint
    cpOut: OutletSystemConnectionPoint


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
s2.cpIn.mapsTo = d2.cpIn

# pass-out from the Equipment to the system
s2.cpOut.mapsTo = d2.cpOut

# dump the result
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
