from bob.core import (
    bind_model_namespace,
    System,
    Device,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    dump,
)

from samples import sample_header

# instances will come from this namespace, otherwise they would be BNode's
__namespace__ = bind_model_namespace("ex", "urn:ex/")


class TestSystem(System):
    cpIn: InletConnectionPoint
    cpOut: OutletConnectionPoint

class TestDevice(Device):
    cpIn: InletConnectionPoint
    cpOut: OutletConnectionPoint
    
# make a system and a device
s1 = TestSystem(label="s1")
d1 = TestDevice(label="d1")
d1 < s1

# pass through the system connection points
s1.cpIn >> s1.cpOut

# make a system and a device
s2 = TestSystem(label="s2")
d2 = TestDevice(label="d2")
d2 < s2

# pass-in from the system to the device
s2.cpIn >> d2.cpIn

# pass-out from the device to the system
d2.cpOut >> s2.cpOut

# dump the result
sample_header("sample011")
dump()
