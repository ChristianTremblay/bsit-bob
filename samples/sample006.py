from pathlib import Path

from bob.core import bind_model_namespace, dump
from bob.connections.air import AirConnection
from bob.systems.archives.hvac import HVACZone1
from bob.systems.archives.vav import VAV2
from bob.systems.archives.heatingcoil import HotWaterCoil2

from header import sample_header


model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# make a sample
hot_water_coil = HotWaterCoil2(label="hot_water_coil")

cold_side_air_connection = AirConnection(label="Cold Air")
hot_side_air_connection = AirConnection(label="Hot Air")

cold_side_air_connection >> hot_water_coil
hot_water_coil >> hot_side_air_connection

# dump the result
sample_header(model_name)
dump()
