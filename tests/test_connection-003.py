from bob.core import bind_model_namespace, dump
from bob.core import Device, ConnectionPoint, Connection
from bob import core
from pathlib import Path
from header import ttl_test_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")
core.INCLUDE_INVERSE = True


def test_connect_from_and_to():
    d1 = Device(label="d1")
    cp1 = ConnectionPoint(d1, label="d1.out")

    d2 = Device(label="d2")
    cp2 = ConnectionPoint(d2, label="d2.in")

    c = Connection()
    c.connect_from(cp1)
    c.connect_to(cp2)
    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
