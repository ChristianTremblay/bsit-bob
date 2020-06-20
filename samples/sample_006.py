from typing import Any

from bob import dump
from bob.air import AirConnection
from bob.hw import HotWaterCoil, HotWaterValve


class HotWaterCoil2(HotWaterCoil):
    """
    This is an example of a hot water coil that contains its valve as a
    subsystem and makes the valve position available as its own connection
    point.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a hot water valve subsystem
        self.hw_valve = HotWaterValve()
        self > self.hw_valve

        # link the hot water pieces together
        self.hw_valve >> self

        # lift the connection
        self.hw_valve_pos = self._connection_points["hw_valve_pos"] = self.hw_valve.pos


# make a sample
hot_water_coil = HotWaterCoil2()

cold_side_air_connection = AirConnection(label="Cold Air")
hot_side_air_connection = AirConnection(label="Hot Air")

cold_side_air_connection >> hot_water_coil
hot_water_coil >> hot_side_air_connection

# dump the result
if __name__ == "__main__":
    dump()
