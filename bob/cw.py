from typing import Any

from .core import (
    ConnectionType,
    register_connection_type,
    Connection,
    InletConnectionPoint,
    OutletConnectionPoint,
    Device,
)
from .air import AirInlet, AirOutlet
from .signal import AnalogIn


class ChilledWater(ConnectionType):
    connection_type: str = "ChilledWater"


@register_connection_type
class ChilledWaterConnection(ChilledWater, Connection):
    pass


class ChilledWaterInlet(InletConnectionPoint, ChilledWater):
    pass


class ChilledWaterOutlet(OutletConnectionPoint, ChilledWater):
    pass


class ChilledWaterValve(Device):
    chilledWaterInlet: ChilledWaterInlet
    chilledWaterOutlet: ChilledWaterOutlet
    position = AnalogIn


class ChilledWaterCoil(Device):
    airInlet: AirInlet
    airOutlet: AirOutlet
    chilledWaterSupply: ChilledWaterInlet
    chilledWaterReturn: ChilledWaterOutlet


class ChilledWaterCoil2(ChilledWaterCoil):
    """
    This is an example of a chilled water coil that contains its valve as a
    subsystem and makes the valve position available as its own connection
    point.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a chilled water valve subsystem
        self.chilled_water_valve = ChilledWaterValve(
            label=self.label + ".chilled_water_valve"
        )
        self > self.chilled_water_valve

        # link the chilled water pieces together
        self.chilled_water_valve >> self

        # lift the position
        self.chilled_water_valve_pos = self.chilled_water_valve.position
