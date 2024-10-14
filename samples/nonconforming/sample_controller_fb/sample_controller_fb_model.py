# import physical_spaces as ps  # isort: skip
import hvac_devices as hd  # isort: skip

# import hvac  # isort: skip

# import lighting_spaces as ls  # isort: skip
# import lighting_devices as ld  # isort: skip
# import lighting  # isort: skip
# import network_devices as nd  # isort: skip
# import electrical_devices as ed  # isort: skip
# import electricity  # isort: skip


import bacnet_references  # isort: skip
import functions  # isort: skip

# import fake_values  # isort: skip

from pathlib import Path
from typing import Any

from bob.assemblage import create_data_and_schema_ttl
from bob.core import bind_model_namespace, data_graph, dump, schema_graph
from bob.scratch.header import sample_header

model_name = Path(__file__).stem
global_ns = Path(__file__).parent.stem
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}/{model_name}/")


# Relations between Physical spaces and Domain spaces

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
