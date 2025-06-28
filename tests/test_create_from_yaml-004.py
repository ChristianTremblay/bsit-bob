from pathlib import Path

from header import ttl_test_header
import pytest
from bob.core import bind_model_namespace, dump
from bob.equipment.hvac.damper import Damper
from bob.template import (
    EquipmentFromTemplate,
    SystemFromTemplate,
    config_from_yaml,
    template_update,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_fail_create_system_from_yaml(bob_fixture):
    yaml_path = Path(__file__).parent / "yaml_templates" / "f4-cvm03050-0.yaml"
    
    with pytest.raises(Exception):
        c = config_from_yaml(str(yaml_path))
        cgm = EquipmentFromTemplate(config=c)


def test_create_system_from_yaml(bob_fixture):
    yaml_path = Path(__file__).parent / "yaml_templates" / "f4-cvm03050-0_noSchema.yaml"
    
    c = config_from_yaml(str(yaml_path))
    cgm = EquipmentFromTemplate(config=c)

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
