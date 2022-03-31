import pytest
from bob.core import (
    bind_model_namespace,
    Device,
    Connection,
    InletConnectionPoint,
    OutletConnectionPoint,
    dump,
)
from pathlib import Path
from header import ttl_test_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_wrong_direction(bob_fixture):
    d1 = Device(label="d1")
    cp1 = OutletConnectionPoint(d1, label="d1.out")

    d2 = Device(label="d2")
    cp2 = InletConnectionPoint(d2, label="d2.in")

    c = Connection()

    with pytest.raises(TypeError):
        c >> cp1

    with pytest.raises(TypeError):
        cp2 >> c

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
