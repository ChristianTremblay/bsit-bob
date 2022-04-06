from pathlib import Path

from header import ttl_test_header

from bob.core import (
    ConnectionPoint,
    Device,
    Junction,
    Segment,
    bind_model_namespace,
    dump,
)

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_segment(bob_fixture):
    d1 = Device(label="d1")
    cp1 = ConnectionPoint(d1)

    j1 = Junction()
    s1 = Segment()
    s1.link_to(j1)
    s1.link_to(cp1)

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
