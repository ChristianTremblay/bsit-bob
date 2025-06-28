from pathlib import Path

from header import ttl_test_header

from bob.core import bind_model_namespace, dump
from bob.equipment.hvac.damper import Damper
from bob.template import (
    ProductGroupFromTemplate,
    SystemFromTemplate,
    config_from_yaml,
    template_update,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_open_yaml(bob_fixture):
    yaml_path = Path(__file__).parent / "yaml_templates" / "ahuAsSystem.yaml"
    c = config_from_yaml(str(yaml_path))
    assert c is not None
    assert isinstance(c, dict)
    assert c["params"]["label"] == "AHU"
    assert c["params"]["comment"] == "AHU delivering air to 2 VAV boxes"


def test_create_system_from_yaml(bob_fixture):
    yaml_path = Path(__file__).parent / "yaml_templates" / "ahuAsSystem.yaml"
    c = config_from_yaml(str(yaml_path))

    ahu = SystemFromTemplate(config=c)

    assert len(ahu._junctions) == 4
    assert len(ahu._equipment) == 9
    assert len(ahu._sensors) == 1

    assert ahu["SA-T"].hasObservationLocation == ahu["SupplyAirDuct"].supplyAir
    c2 = config_from_yaml(str(yaml_path))
    ahu2 = ProductGroupFromTemplate(
        config=c2, label="AHU2", comment="Second AHU", model="ACMESystem"
    )

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
