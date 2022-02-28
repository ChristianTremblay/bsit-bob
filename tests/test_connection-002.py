from bob.core import bind_model_namespace, dump
from bob.core import Device, ConnectionPoint, Connection
from bob import core
from pathlib import Path
from header import ttl_test_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")
core.INCLUDE_INVERSE = True


def test_connect_from():
    d1 = Device(label="d1")
    cp1 = ConnectionPoint(d1)

    c = Connection()
    c.connect_from(cp1)
    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
