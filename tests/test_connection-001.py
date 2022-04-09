from pathlib import Path

from header import ttl_test_header

from bob import core
from bob.core import (
    Connection,
    Device,
    InletConnectionPoint,
    bind_model_namespace,
    dump,
)

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")

core.INCLUDE_INVERSE = True


def test_connect_to(bob_fixture):
    d1 = Device(label="d1")
    cp1 = InletConnectionPoint(d1)

    c = Connection()
    c >> cp1

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
