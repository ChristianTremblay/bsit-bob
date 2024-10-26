from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.core import (
    bind_model_namespace,
)

# Prototypes
from bob.scratch.header import sample_header
from bob.scratch.hvac.heatpump import AirToAirHeatPump

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex:{model_name}/")

hp_system = AirToAirHeatPump(label="MyAir2AirHeatPump")
_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
