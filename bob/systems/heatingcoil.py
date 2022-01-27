from typing import Any

from ..connections.water import (
    HotWaterInletSystemConnectionPoint,
    HotWaterOutletSystemConnectionPoint,
)

from ..core import s223, System

from ..connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)

from ..connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)
from ..devices.hvac.coil import ElectricalHeatingCoil
from ..devices.hvac.scr import SCR
from ..devices.hvac.valve import HotWaterValve

from ..signal import AnalogIn

__namespace__ = s223


class ElectricalHeatingCoilWithSCR(System):
    """
    This is an example of an electrical heating coil with a SCR.
    """

    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    powerInlet: ElectricalInletConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a electrical heating coil
        self.electrical_heating_coil = ElectricalHeatingCoil(
            label=self.label + ".elechtg_coil"
        )
        self.airInlet.mapsTo = self.electrical_heating_coil.airInlet
        self.airOutlet.mapsTo = self.electrical_heating_coil.airOutlet

        # create a SCR to modulate the coil
        self.scr = SCR(label=self.label + ".elechtg_scr")
        self.powerInlet.mapsTo = self.scr.powerInlet
        self.scr.powerOutlet.mapsTo = self.electrical_heating_coil.powerInlet
        self.scr >> self.electrical_heating_coil

        # reference the SCR modulation command
        self.scr_modulation = self.scr.modulation


class HotWaterCoil(System):
    """
    This is an example of a hot water coil that contains its valve as a
    subsystem and makes the valve position available as its own connection
    point.
    """

    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    hotWaterInlet: HotWaterInletSystemConnectionPoint
    hotWaterOutlet: HotWaterOutletSystemConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a hot water coil
        self.hot_water_coil = HotWaterCoil(label=self.label + ".hw_coil")
        self.airInlet.mapsTo = self.hot_water_coil.airInlet
        self.airOutlet.mapsTo = self.hot_water_coil.airOutlet

        # create a hot water valve
        self.hot_water_valve = HotWaterValve(label=self.label + ".hw_valve")
        self.hotWaterInlet.mapsTo = self.hot_water_valve.hotWaterInlet
        self.hot_water_valve >> self.hot_water_coil
        self.hotWaterOutlet.mapsTo = self.hot_water_coil.hotWaterOutlet

        # reference the valve position
        self.hot_water_valve_pos = self.hot_water_valve.position
