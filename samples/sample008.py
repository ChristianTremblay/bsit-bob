from pathlib import Path

from header import sample_header

from bob.core import (
    ConnectionPoint,
    Device,
    System,
    SystemConnectionPoint,
    bind_model_namespace,
    dump,
)

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class TestDevice(Device):
    cp: ConnectionPoint


class TestSystem(System):
    cp: SystemConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        device = TestDevice(label=kwargs["label"] + "-d")
        self.cp.mapsTo = device.cp


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

s1.cp >> s2.cp

# s1 is connected to s2
s1 = TestSystem(label="5-s1")
s2 = TestSystem(label="5-s2")
s1 >> s2

# dump the result
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
