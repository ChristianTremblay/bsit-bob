from pathlib import Path

from header import sample_header

from bob.core import (
    bind_model_namespace,
    data_graph,
    schema_graph,
    dump,
    Equipment,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    OutletSystemConnectionPoint,
    System,
)
from bob.connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class TestEquipment(Equipment):
    cp: AirInletConnectionPoint


class TestSystem(System):
    cpI: AirInletSystemConnectionPoint
    cpO: AirOutletSystemConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        equipment = TestEquipment(label=kwargs["label"] + "-d")
        self.cpI.mapsTo = equipment.cp


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

# dump the result
dump(data_graph, filename=f"samples/ttl/{model_name}.data.ttl", header=sample_header(model_name))
dump(schema_graph, filename=f"samples/ttl/{model_name}.schema.ttl")

