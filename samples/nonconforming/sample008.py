from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.core import (
    BoundaryConnectionPoint,
    Equipment,
    InletConnectionPoint,
    System,
    bind_model_namespace,
    data_graph,
    dump,
    schema_graph,
)
from bob.scratch.header import sample_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class TestEquipment(Equipment):
    cp: AirInletConnectionPoint


class TestSystem(System):
    cpI: BoundaryConnectionPoint
    cpO: BoundaryConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        equipment = TestEquipment(label=kwargs["label"] + "-d")
        self.cpI = equipment.cp


# two independant systems
s1 = TestSystem(label="1-s1")
s2 = TestSystem(label="1-s2")

# s1 is a subsystem of s2
s1 = TestSystem(label="2-s1")
s2 = TestSystem(label="2-s2")

s1 < s2

# s1 is a supersystem of s2
s1 = TestSystem(label="3-s1")
s2 = TestSystem(label="3-s2")

s1 > s2

# s1 is connected to s2
s1 = TestSystem(label="4-s1")
s2 = TestSystem(label="4-s2")

# s1 >> s2

# s2 is connected to s1
s1 = TestSystem(label="5-s1")
s2 = TestSystem(label="5-s2")
# s2 >> s1

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
