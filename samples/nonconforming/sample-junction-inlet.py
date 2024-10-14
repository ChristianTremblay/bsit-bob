from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.core import (
    Equipment,
    Junction,
    bind_model_namespace,
    data_graph,
    dump,
    schema_graph,
)
from bob.scratch.header import sample_header

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

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
