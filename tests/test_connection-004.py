from bob.core import bind_model_namespace, dump, turtle
from bob.node import (
    Device,
    ConnectionPoint,
    Connection,
    InletConnectionPoint,
    OutletConnectionPoint,
)

__namespace__ = bind_model_namespace("ex", "urn:ex/")

d1 = Device(label="d1")
cp1 = OutletConnectionPoint(d1, label="d1.out")

d2 = Device(label="d2")
cp2 = InletConnectionPoint(d2, label="d2.in")

c = Connection()
c.connect_from(cp1)
c.connect_to(cp2)

result = turtle()
dump()


def test_result():
    print(result)
