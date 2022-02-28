from bob.core import bind_model_namespace, dump
from bob.core import Junction
from pathlib import Path
from header import ttl_test_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_link_junction_to_junction():
    j1 = Junction()
    j2 = Junction()
    j1.link_to(j2)

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
