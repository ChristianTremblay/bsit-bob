import logging
from pathlib import Path

from bob.scratch.header import sample_header
from bob.assemblage import create_data_and_schema_ttl
from bob.core import (
    bind_model_namespace,
)
from bob.scratch.hvac.boiler import DomesticHPWaterHeater

_log = logging.getLogger(__name__)

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex:{model_name}/")

VALIDATE = True

hpwh = DomesticHPWaterHeater(label="hp_waterheater")


_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
