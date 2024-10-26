import logging
from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.core import bind_model_namespace
from bob.equipment.hvac.boiler import DomesticHotWaterHeater
from bob.equipment.hvac.boiler import (
    DomesticHotWaterHeater as BobDomesticElectricalWaterHeater,
)
from bob.scratch.header import sample_header
from bob.scratch.hvac.boiler import (
    DomesticHotWaterHeater as ScratchDomesticHotWaterHeater,
)

_log = logging.getLogger(__name__)

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex:{model_name}/")

hwh1 = ScratchDomesticHotWaterHeater(label="Scratch Electric Water Heater")
hwh2 = BobDomesticElectricalWaterHeater(label="Bob Electric Water Heater")
hwh3 = DomesticHotWaterHeater(label="Generic Electric Water Heater")


_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
