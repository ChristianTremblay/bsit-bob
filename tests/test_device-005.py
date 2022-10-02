from pathlib import Path

from header import ttl_test_header

from bob.connections.electricity import ElectricalInletConnectionPoint
from bob.core import Device, bind_model_namespace, dump
from bob.equipments.hvac import Fan

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_fan(bob_fixture):
    _config = {
        "params": {
            "label": "VA-1",
            "comment": "Supply Fan",
            "electricalInlet": ElectricalInletConnectionPoint,
        },
        "sensors": {},
        "devices": {("VA1-VFD", Device): {"comment": "VFD for VA-1"}},
    }
    fan1 = Fan(
        config=_config,
    )

    fan2 = Fan(
        label="VA-2",
        electricalInlet=ElectricalInletConnectionPoint,
    )

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
