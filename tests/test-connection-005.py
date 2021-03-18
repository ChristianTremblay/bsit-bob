from bob.core import (
    bind_model_namespace,
    Device,
    InletConnectionPoint,
    OutletConnectionPoint,
    Connection,
    dump,
)

__namespace__ = bind_model_namespace("ex", "urn:ex/")

d1 = Device(label="d1")
cp1 = OutletConnectionPoint(d1, label="d1.out")

d2 = Device(label="d2")
cp2 = InletConnectionPoint(d2, label="d2.in")

c = Connection()

try:
    c.connect_to(cp1)
except Exception as err:
    print(f"exception caught: {err}")

try:
    c.connect_from(cp2)
except Exception as err:
    print(f"exception caught: {err}")
