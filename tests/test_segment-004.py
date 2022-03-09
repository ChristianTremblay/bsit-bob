from bob.core import bind_model_namespace, dump
from bob.core import Junction, Device, ConnectionPoint
from pathlib import Path
from header import ttl_test_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_segment_004(bob_fixture):
    d1 = Device(label="d1")
    cp1 = ConnectionPoint(d1)

    j1 = Junction()
    cp1.link_to(j1)

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
