from pathlib import Path

from header import ttl_test_header

from bob.core import bind_model_namespace, dump
from bob.externalreference.bacnet import BACnetExternalReference

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_external_reference(bob_fixture):
    ref1 = BACnetExternalReference("bacnet://12345/analog-value,1/present-value", label="ref1")

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
