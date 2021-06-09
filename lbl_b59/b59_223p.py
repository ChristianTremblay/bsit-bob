from pathlib import Path

from bob import bind_model_namespace, dump
from bob.air import Zone
from bob.vav import VAV1

from samples.header import sample_header


model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")

print("Testing Joel's builder")

# setup B59 floors

# TODO

# setup 3rd floor Zones
# TODO

# setup 4th floor Zones
# TODO

g_f_perimeter_zone = Zone(label="Perimeter Zone Ground Floor")
vav = VAV1(label="Zone.VAV")

# connect the output of the VAV box to the input of the Zone
vav >> g_f_perimeter_zone

# dump the result
sample_header(model_name)
dump()
