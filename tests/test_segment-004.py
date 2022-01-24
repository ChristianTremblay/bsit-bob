from bob.core import bind_model_namespace, dump, turtle

from bob.node import Junction, Segment, Device, ConnectionPoint

__namespace__ = bind_model_namespace("ex", "urn:ex/")

d1 = Device(label="d1")
cp1 = ConnectionPoint(d1)

j1 = Junction()
cp1.link_to(j1)


result = turtle()
dump()


def test_result():
    print(result)
