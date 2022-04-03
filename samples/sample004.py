from pathlib import Path

from bob.core import bind_model_namespace, dump
from bob.systems.hvac.vav import VAV
from bob.space.hvac import HVACZone

from header import sample_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# there is a zone that contains a space
zone = HVACZone(label="Zone")

# there is a VAV box
vav_template = {
    "params": {"label": "VAV1", "comment": "A VAV Box as a system"},
    "sensors": {},
    "devices": {},
}
vav = VAV(config=vav_template)

# connect the output of the VAV box to the input of the Zone
vav.airOutlet.mapsTo = zone.airInlet

# dump the result
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
