from pathlib import Path

from header import sample_header

from bob.core import bind_model_namespace, dump
from bob.equipments.hvac.damper import Damper
from bob.equipments.hvac.vav import VAV
from bob.space.hvac import HVACSpace, HVACZone

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# there is a zone that contains a space
zone = HVACZone(label="Zone")

# create a space
domain_space = HVACSpace(label="Domain_Space")
zone > domain_space

# reference the connections
zone.airInlet.mapsTo = domain_space.ductAirInlet
zone.airOutlet.mapsTo = domain_space.ductAirOutlet

# there is a VAV box
vav_template = {
    "params": {"label": "VAV1", "comment": "A VAV Box as a system"},
    "sensors": {},
    "equipments": {},
}
vav = VAV(config=vav_template)

# create a damper
damper = Damper(label="VAV1.damper")
vav > damper

# reference the connections
vav.airInlet.mapsTo = damper.airInlet
vav.airOutlet.mapsTo = damper.airOutlet


# connect the output of the VAV box to the input of the Zone
vav.airOutlet >> zone.airInlet

# dump the result
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
