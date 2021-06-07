from pathlib import Path

from bob import bind_model_namespace, dump
from bob.air import HVACZone
from bob.vav import VAV1

from header import sample_header


model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# there is a zone that contains a space
zone = HVACZone(label="Zone")

# there is a VAV box
vav = VAV1(label="Zone.VAV")

# connect the output of the VAV box to the input of the Zone
vav >> zone

# dump the result
sample_header(model_name)
dump()
