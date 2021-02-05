from typing import Any

from .core import (
    c223,
    ConnectionType,
    register_connection_type,
    Connection,
    Device,
    InletConnectionPoint,
    OutletConnectionPoint,
    System,
    SystemInletConnectionPoint,
    SystemOutletConnectionPoint,
)
from .air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from .signal import AnalogIn

__namespace__ = c223


class ChilledWater(ConnectionType):
    connection_type: str = "ChilledWater"


@register_connection_type
class ChilledWaterConnection(ChilledWater, Connection):
    pass


class ChilledWaterInlet(InletConnectionPoint, ChilledWater):
    pass


class ChilledWaterOutlet(OutletConnectionPoint, ChilledWater):
    pass


class ChilledWaterSystemInlet(SystemInletConnectionPoint, ChilledWater):
    pass


class ChilledWaterSystemOutlet(SystemOutletConnectionPoint, ChilledWater):
    pass


class ChilledWaterValve(Device):
    chilledWaterInlet: ChilledWaterInlet
    chilledWaterOutlet: ChilledWaterOutlet
    position = AnalogIn


class ChilledWaterCoil(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    chilledWaterInlet: ChilledWaterInlet
    chilledWaterOutlet: ChilledWaterOutlet


class ChilledWaterCoil2(System):
    """
    This is an example of a chilled water coil that contains its valve as a
    subsystem and makes the valve position available as its own connection
    point.
    """

    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    chilledWaterSupply: ChilledWaterSystemInlet
    chilledWaterReturn: ChilledWaterSystemOutlet

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a hot water coil
        self.chilled_water_coil = ChilledWaterCoil(label=self.label + ".cw_coil")
        self.airInlet > self.chilled_water_coil.airInlet
        self.airOutlet > self.chilled_water_coil.airOutlet

        # create a hot water valve
        self.chilled_water_valve = ChilledWaterValve(label=self.label + ".cw_valve")
        self.chilledWaterSupply > self.chilled_water_valve.chilledWaterInlet
        self.chilled_water_valve >> self.chilled_water_coil
        self.chilledWaterReturn > self.chilled_water_coil.chilledWaterOutlet

        # reference the valve position
        self.chilled_water_valve_pos = self.chilled_water_valve.position
