from pathlib import Path

from bob import bind_model_namespace, dump
from bob.air import Zone
from bob.vav import VAV1

from header import sample_header


model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


zone = Zone(label="Zone")
vav = VAV1(label="Zone.VAV")

# connect the output of the VAV box to the input of the Zone
vav >> zone

# dump the result
sample_header(model_name)
dump()
