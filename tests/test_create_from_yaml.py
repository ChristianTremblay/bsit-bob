from pathlib import Path

from header import ttl_test_header

from bob.core import bind_model_namespace, dump
from bob.equipment.hvac.damper import Damper
from bob.template import SystemFromTemplate, template_update, config_from_yaml

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")

def test_open_yaml(bob_fixture):
    yaml_path = Path(__file__).parent / "yaml_templates" / "ahu.yaml"
    c = config_from_yaml(str(yaml_path))
    assert c is not None
    assert isinstance(c, dict)
    assert c["params"]["label"] == "AHU"
    assert c["params"]["comment"] == "AHU delivering air to 2 VAV boxes"

def test_create_system_from_yaml(bob_fixture):
    yaml_path = Path(__file__).parent / "yaml_templates" / "ahu.yaml"
    c = config_from_yaml(str(yaml_path))
    
    ahu = SystemFromTemplate(config=c)
    assert ahu['SA-T'].hasObservationLocation == ahu['supplyAir']
    assert len(ahu._connections) == 4
    assert len(ahu._equipment) == 10
    assert len(ahu._sensors) == 1



