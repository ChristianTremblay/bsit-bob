from pathlib import Path

from bob.core import (
    bind_model_namespace,
    Device,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    System,
    SystemConnectionPoint,
    SystemInletConnectionPoint,
    SystemOutletConnectionPoint,
    dump,
)

from header import sample_header


model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class TestSystem(System):
    cpIn: SystemInletConnectionPoint
    cpOut: SystemOutletConnectionPoint


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
d2.cpIn < s2.cpIn

# pass-out from the device to the system
s2.cpOut < d2.cpOut

# dump the result
sample_header(model_name)
dump()
