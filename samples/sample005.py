from pathlib import Path

from bob.core import bind_model_namespace, dump
from bob.connections.air import AirConnection
from bob.systems.archives.hvac import HVACZone1
from bob.systems.archives.vav import VAV2

# from header import sample_header


model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# create Zone-1 and its VAV connected together
zone1 = HVACZone1(label="Zone-1")
vav1 = VAV2(label="Zone-1.VAV")
vav1 >> zone1

# create Zone-2 and its VAV connected together
zone2 = HVACZone1(label="Zone-2")
vav2 = VAV2(label="Zone-2.VAV")
vav2 >> zone2

# common supply connection shared
supply_air = AirConnection(label="SupplyAir")
supply_air >> vav1
supply_air >> vav2

# similar for return air
return_air = AirConnection(label="ReturnAir")
zone1 >> return_air
zone2 >> return_air

# dump the result
# sample_header(model_name)
dump()
