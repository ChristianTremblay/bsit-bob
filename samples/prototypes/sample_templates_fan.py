from pathlib import Path

from header import sample_header
from bob.core import UNIT, Role, bind_model_namespace, data_graph, dump, schema_graph
from bob.template import SystemFromTemplate
from bob.equipment.hvac.fan import Fan as BasicFan
from bob.scratch.hvac.fan import (
    Fan,
    system_600VFan_with_Starter_template,
    system_600VFan_with_VFD_template,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")

f1 = Fan(label="Basic Fan")
f2 = SystemFromTemplate(
    label="Fan with Starter", config=system_600VFan_with_Starter_template
)
f3 = SystemFromTemplate(label="Fan with VFD", config=system_600VFan_with_VFD_template)

f4 = BasicFan(label="A Bob Fan")
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
