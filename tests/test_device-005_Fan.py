from bob.core import (
    bind_model_namespace,
    Device,
    dump,
)

from bob.devices.hvac import Fan

from pathlib import Path

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


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

dump()
