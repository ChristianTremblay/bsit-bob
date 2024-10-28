from pathlib import Path

from header import ttl_test_header

from bob import core
from bob.assemblage import create_data_and_schema_ttl, model_namespace
from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.core import (
    BoundaryConnectionPoint,
    Equipment,
    System,
    bind_model_namespace,
    dump,
)
from bob.scratch.header import sample_header
from bob.scratch.hvac.vav import VAV, vav_withelectricreheat_template

model_name, global_ns = model_namespace(__file__)
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}:{model_name}/")

v = VAV(config=vav_withelectricreheat_template, label="VAV with Electrical Reheat")

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
