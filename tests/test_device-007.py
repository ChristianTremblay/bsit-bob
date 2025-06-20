from pathlib import Path

from header import ttl_test_header

from bob import schemaorg
from bob.connections.electricity import ElectricalInletConnectionPoint
from bob.core import Equipment, bind_model_namespace, dump
from bob.equipment.hvac.fan import Fan

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class MyFan(Fan, schemaorg.Product):
    pass


def test_create_fan_as_schemaor_product(bob_fixture):
    _config = {
        "params": {
            "label": "VA-1",
            "comment": "Supply Fan",
            "electricalInlet": ElectricalInletConnectionPoint,
        },
        "sensors": {},
        "equipment": {("VA1-VFD", Equipment): {"comment": "VFD for VA-1"}},
    }
    fan1 = MyFan(
        config=_config,
        model="BALDOR 5KCF8",
    )

    fan2 = MyFan(
        label="VA-2",
        model="BALDOR 5KCF8",
        electricalInlet=ElectricalInletConnectionPoint,
    )

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
