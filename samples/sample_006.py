from bob import dump
from bob.air import AirConnection
from bob.hw import HotWaterCoil2


# make a sample
hot_water_coil = HotWaterCoil2(label="hot_water_coil")

cold_side_air_connection = AirConnection(label="Cold Air")
hot_side_air_connection = AirConnection(label="Hot Air")

cold_side_air_connection >> hot_water_coil
hot_water_coil >> hot_side_air_connection

# dump the result
if __name__ == "__main__":
    dump()
