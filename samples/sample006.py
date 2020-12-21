from bob import bind_model_namespace, dump
from bob.air import AirConnection
from bob.hw import HotWaterCoil2

from samples import sample_header

# instances will come from this namespace, otherwise they would be BNode's
bind_model_namespace("ex", "urn:ex/")

# make a sample
hot_water_coil = HotWaterCoil2(label="hot_water_coil")

cold_side_air_connection = AirConnection(label="Cold Air")
hot_side_air_connection = AirConnection(label="Hot Air")

cold_side_air_connection >> hot_water_coil
hot_water_coil >> hot_side_air_connection

# dump the result
sample_header("sample006")
dump()
