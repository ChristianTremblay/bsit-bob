from bob import bind_model_namespace, dump
from bob.air import Zone
from bob.vav import VAV1

from samples import sample_header

# instances will come from this namespace, otherwise they would be BNode's
bind_model_namespace("ex", "urn:ex/")

zone = Zone(label="Zone")
vav = VAV1(label="Zone.VAV")

# connect the output of the VAV box to the input of the Zone
vav >> zone

# dump the result
if __name__ == "__main__":
    sample_header("sample004")
    dump()
