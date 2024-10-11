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

from bob.scratch.header import sample_header

from bob.core import bind_model_namespace, data_graph, dump, schema_graph

model_name = Path(__file__).stem
global_ns = Path(__file__).parent.stem
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}/{model_name}/")


# Relations between Physical spaces and Domain spaces

dump(
    data_graph,
    filename=f"samples/ttl/{model_name}.data.ttl",
    header=sample_header(model_name, "data"),
)
dump(
    schema_graph,
    filename=f"samples/ttl/{model_name}.schema.ttl",
    header=sample_header(model_name, "schema"),
)
