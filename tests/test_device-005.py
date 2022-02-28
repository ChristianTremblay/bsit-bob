from bob.core import (
    bind_model_namespace,
    Device,
    dump,
)

from bob.devices.hvac import Fan

from pathlib import Path
from header import ttl_test_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_fan():
    _config = {
        "params": {"label": "VA-1", "comment": "Supply Fan"},
        "sensors": {},
        "contains": {("VA1-VFD", Device): {"comment": "VFD for VA-1"}},
    }
    fan1 = Fan(
        config=_config,
    )

    fan2 = Fan(
        label="VA-2",
    )

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
