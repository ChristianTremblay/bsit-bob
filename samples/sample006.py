from pathlib import Path

from header import sample_header

from bob.connections.air import AirConnection
from bob.core import bind_model_namespace, dump
from bob.systems.archives.heatingcoil import HotWaterCoil2
from bob.systems.archives.hvac import HVACZone1
from bob.systems.archives.vav import VAV2

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# make a sample
hot_water_coil = HotWaterCoil2(label="hot_water_coil")

cold_side_air_connection = AirConnection(label="Cold Air")
hot_side_air_connection = AirConnection(label="Hot Air")

cold_side_air_connection >> hot_water_coil.airInlet
hot_water_coil.airOutlet >> hot_side_air_connection

# dump the result
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
