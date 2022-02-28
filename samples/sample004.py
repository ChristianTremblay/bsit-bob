from pathlib import Path

from bob.core import bind_model_namespace, dump
from bob.systems.archives.vav import VAV1
from bob.systems.archives.hvac import HVACZone1

from header import sample_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# there is a zone that contains a space
zone = HVACZone1(label="Zone")

# there is a VAV box
vav = VAV1(label="Zone.VAV")

# connect the output of the VAV box to the input of the Zone
vav >> zone

# dump the result
sample_header(model_name)
dump()
