from bob.core import bind_model_namespace, dump, turtle
from bob.node import Device, ConnectionPoint, Connection

__namespace__ = bind_model_namespace("ex", "urn:ex/")

d1 = Device(label="d1")
cp1 = ConnectionPoint(d1)

c = Connection()
c.connect_from(cp1)

result = turtle()
dump()


def test_result():
    print(result)
