from bob.core import bind_model_namespace, turtle, dump
from bob.core import Device, ConnectionPoint, Connection
from bob import core

__namespace__ = bind_model_namespace("ex", "urn:ex/")

core.RECIPROCITY_RELATION = True
d1 = Device(label="d1")
cp1 = ConnectionPoint(d1)

c = Connection()
c.connect_to(cp1)

result = turtle()
dump()


def test_result():
    print(result)
