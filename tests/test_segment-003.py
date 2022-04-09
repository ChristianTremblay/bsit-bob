from pathlib import Path

from header import ttl_test_header

from bob.core import InletConnectionPoint, Device, Segment, bind_model_namespace, dump

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_segment_003(bob_fixture):
    d1 = Device(label="d1")
    cp1 = InletConnectionPoint(d1)

    s1 = Segment()
    cp1.link_to(s1)

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
