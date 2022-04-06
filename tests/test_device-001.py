from pathlib import Path

from header import ttl_test_header

from bob.core import Device, Property, bind_model_namespace, dump

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_devices(bob_fixture):
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

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
