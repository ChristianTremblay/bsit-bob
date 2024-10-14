from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.core import PhysicalSpace, bind_model_namespace, data_graph, dump, schema_graph
from bob.equipment.hvac.damper import Damper
from bob.equipment.hvac.vav import VAV
from bob.scratch.header import sample_header
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

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
