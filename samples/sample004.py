from pathlib import Path

from bob.core import bind_model_namespace, data_graph, schema_graph, dump
from bob.scratch.header import sample_header

from bob.core import PhysicalSpace
from bob.equipment.hvac.damper import Damper
from bob.equipment.hvac.vav import VAV
from bob.space.hvac import HVACSpace, HVACZone

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# there is a zone that contains the space
zone = HVACZone(label="Zone")

# there is a room that contains the space
room = PhysicalSpace(label="Room 191")

# create the space
domain_space = HVACSpace(label="Domain_Space")
zone > domain_space
room > domain_space

# reference the connections
# TODO : System don't have CP anymore Make VAV an equipment
# zone.airInlet.mapsTo = domain_space.ductAirInlet
# zone.airOutlet.mapsTo = domain_space.ductAirOutlet

# there is a VAV box
vav_template = {
    "params": {"label": "VAV1", "comment": "A VAV Box as a system"},
    "sensors": {},
    "equipment": {},
}
vav = VAV(config=vav_template)

# connect the output of the VAV box to the input of the Zone
# vav.airOutlet >> zone.airInlet

# dump the result
dump(
    data_graph,
    filename=f"samples/ttl/{model_name}.data.ttl",
    header=sample_header(model_name),
)
dump(schema_graph, filename=f"samples/ttl/{model_name}.schema.ttl")
