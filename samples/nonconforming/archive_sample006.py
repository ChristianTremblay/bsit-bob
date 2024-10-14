from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.connections.air import AirConnection
from bob.core import bind_model_namespace, dump
from bob.equipment.archives.heatingcoil import HotWaterCoil2
from bob.equipment.archives.hvac import HVACZone1
from bob.equipment.archives.vav import VAV2
from bob.scratch.header import sample_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# make a sample
hot_water_coil = HotWaterCoil2(label="hot_water_coil")

cold_side_air_connection = AirConnection(label="Cold Air")
hot_side_air_connection = AirConnection(label="Hot Air")

cold_side_air_connection >> hot_water_coil.airInlet
hot_water_coil.airOutlet >> hot_side_air_connection

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
