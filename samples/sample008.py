from pathlib import Path

from header import sample_header

from bob.core import (
    Device,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    OutletSystemConnectionPoint,
    System,
    bind_model_namespace,
    dump,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class TestDevice(Device):
    cp: InletConnectionPoint


class TestSystem(System):
    cpI: InletSystemConnectionPoint
    cpO: OutletSystemConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        device = TestDevice(label=kwargs["label"] + "-d")
        self.cpI.mapsTo = device.cp


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
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
