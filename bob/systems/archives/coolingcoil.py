from typing import Any

from ..core import s223, System


from ..connections.air import (
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)

from ..connections.water import (
    ChilledWaterInletSystemConnectionPoint,
    ChilledWaterOutletSystemConnectionPoint,
)
from ..devices.hvac.coil import ChilledWaterCoil
from ..devices.hvac.valve import ChilledWaterValve
from ..signal import AnalogIn

__namespace__ = s223


class ChilledWaterCoil2(System):
    """
    This is an example of a chilled water coil that contains its valve as a
    subsystem and makes the valve position available as its own connection
    point.
    """

    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    chilledWaterSupply: ChilledWaterInletSystemConnectionPoint
    chilledWaterReturn: ChilledWaterOutletSystemConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a chilled water coil
        self.chilled_water_coil = ChilledWaterCoil(label=self.label + ".cw_coil")
        self.airInlet.mapsTo = self.chilled_water_coil.airInlet
        self.airOutlet.mapsTo = self.chilled_water_coil.airOutlet

        # create a chilled water valve
        self.chilled_water_valve = ChilledWaterValve(label=self.label + ".cw_valve")
        self.chilledWaterSupply.mapsTo = self.chilled_water_valve.chilledWaterInlet
        self.chilledWaterReturn.mapsTo = self.chilled_water_coil.chilledWaterOutlet

        # connect the valve to the coil
        self.chilled_water_valve >> self.chilled_water_coil

        # reference the valve position
        self.chilled_water_valve_pos = self.chilled_water_valve.position
