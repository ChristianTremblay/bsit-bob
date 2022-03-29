from bob.core import bind_model_namespace, dump
from bob.core import (
    Device,
    Connection,
    InletConnectionPoint,
    OutletConnectionPoint,
)
from bob import core
from pathlib import Path
from header import ttl_test_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")
core.INCLUDE_INVERSE = True


def test_connection_with_direction(bob_fixture):
    d1 = Device(label="d1")
    cp1 = OutletConnectionPoint(d1, label="d1.out")

    d2 = Device(label="d2")
    cp2 = InletConnectionPoint(d2, label="d2.in")

    c = Connection()
    cp1 >> c >> cp2
    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
