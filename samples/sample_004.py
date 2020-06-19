from bob import dump
from bob.air import Zone
from bob.vav import VAV1

zone = Zone(name="Zone")
vav = VAV1(name="Zone.VAV")

# connect the output of the VAV box to the input of the Zone
vav >> zone

# dump the result
if __name__ == "__main__":
    dump()
