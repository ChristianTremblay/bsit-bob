from pathlib import Path

from header import sample_header
from bob.core import UNIT, Role, bind_model_namespace, data_graph, dump, schema_graph
from bob.template import template_update, configure_relations
from bob.equipment.hvac.fan import Fan, fan_with_starter_template, fan_with_vfd_template

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")

f1 = Fan(label="Basic Fan")
f2 = Fan(label="Fan with Starter", config=fan_with_starter_template)
f3 = Fan(label="Fan with VFD", config=fan_with_vfd_template)

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
