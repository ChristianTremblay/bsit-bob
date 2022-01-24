from bob.core import bind_model_namespace, dump, turtle
from bob.node import Junction, Segment, Device, ConnectionPoint

__namespace__ = bind_model_namespace("ex", "urn:ex/")

j1 = Junction()
j2 = Junction()
j1.link_to(j2)

result = turtle()
dump()


def test_result():
    print(result)
