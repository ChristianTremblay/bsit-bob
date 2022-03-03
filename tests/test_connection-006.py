from pathlib import Path

from bob.core import (
    bind_model_namespace,
    dump,
)
from bob.connections import (
    ChilledWaterConnection,
)

from bob.devices.hvac import Fan, ChilledWaterCoil

# from header import sample_header


model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# there is a chilled water connection, we don't know where the chilled
# is coming from
c = ChilledWaterConnection()

# there is a chilled water coil (itself a system) that is a subsystem
# of a larger context
coil1 = ChilledWaterCoil(label="CW-Coil-1")

# the coil gets its chilled water from the connection
c >> coil1

# there is a fan, and the air output of the fan goes into the coil
f = Fan(label="F")
f >> coil1

dump()
