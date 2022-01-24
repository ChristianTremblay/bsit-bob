from bob.core import bind_model_namespace, dump, turtle
from bob.node import Device, Property

__namespace__ = bind_model_namespace("ex", "urn:ex/")

d1 = Device(label="d1")


class TestDevice2(Device):
    pass


d2 = TestDevice2(label="d2")


class TestProperty(Property):
    pass


class TestDevice3(Device):
    prop: TestProperty


d3 = TestDevice3(label="d3")

d3.prop = TestProperty(1)

dump()
result = turtle()


def test_result():
    print(result)
