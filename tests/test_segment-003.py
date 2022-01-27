from bob.core import bind_model_namespace, dump, turtle
from bob.core import Junction, Segment, Device, ConnectionPoint

__namespace__ = bind_model_namespace("ex", "urn:ex/")

d1 = Device(label="d1")
cp1 = ConnectionPoint(d1)

s1 = Segment()
cp1.link_to(s1)

result = turtle()
dump()


def test_result():
    print(result)
