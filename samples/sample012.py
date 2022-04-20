from pathlib import Path

from header import sample_header

from bob.core import (
    Device,
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


class TestDevice(Device):
    cpIn: InletConnectionPoint
    cpOut: OutletConnectionPoint


# make a system and a device
s1 = TestSystem(label="s1")
d1 = TestDevice(label="d1")
d1 < s1

# make a system and a device
s2 = TestSystem(label="s2")
d2 = TestDevice(label="d2")
d2 < s2

# pass-in from the system to the device
s2.cpIn.mapsTo = d2.cpIn

# pass-out from the device to the system
s2.cpOut.mapsTo = d2.cpOut

# dump the result
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
