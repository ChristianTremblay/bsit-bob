from pathlib import Path

from header import ttl_test_header

from bob.core import (
    Device,
    InletConnectionPoint,
    Junction,
    OutletConnectionPoint,
    bind_model_namespace,
    dump,
)

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_connect_junction_to_cp(bob_fixture):
    d1 = Device(label="d1")
    cp1 = OutletConnectionPoint(d1)

    d2 = Device(label="d2")
    cp2 = InletConnectionPoint(d2)

    j1 = Junction()
    j1.link_to(cp1)
    j1.link_to(cp2)

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
