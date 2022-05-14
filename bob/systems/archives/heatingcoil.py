from typing import Any

from bob.properties import Percent

from ...connections.air import (
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)
from ...connections.water import (
    HotWaterInletConnectionPoint,
    HotWaterInletSystemConnectionPoint,
    HotWaterOutletConnectionPoint,
    HotWaterOutletSystemConnectionPoint,
)
from ...core import Device, System, s223
from ...devices.hvac.coil import ElectricalHeatingCoil
from ...devices.hvac.scr import SCR
from ...devices.hvac.valve import TwoWayValve

_namespace = s223


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


class HotWaterCoil(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    hotWaterSupply: HotWaterInletConnectionPoint
    hotWaterReturn: HotWaterOutletConnectionPoint


class HotWaterCoil2(System):
    """
    This is an example of a hot water coil that contains a hot water valve
    device and makes the valve position available as its own analog output
    signal.
    """

    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    hotWaterSupply: HotWaterInletSystemConnectionPoint
    hotWaterReturn: HotWaterOutletSystemConnectionPoint
    hotWaterValvePosition: Percent

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a hot water coil
        self.hot_water_coil = HotWaterCoil(label=self.label + ".hw_coil")
        self.airInlet.mapsTo = self.hot_water_coil.airInlet
        self.airOutlet.mapsTo = self.hot_water_coil.airOutlet

        # create a hot water valve
        self.hot_water_valve = TwoWayValve(
            label=self.label + ".hw_valve",
            # waterInlet=HotWaterInletConnectionPoint,
            # waterOutlet=HotWaterOutletConnectionPoint,
            # feedback=0,
        )
        self.hotWaterSupply.mapsTo = self.hot_water_valve.waterInlet
        self.hot_water_valve >> self.hot_water_coil
        self.hotWaterReturn.mapsTo = self.hot_water_coil.hotWaterReturn

        # reference the valve position
        # self.hotWaterValvePosition = self.hot_water_valve.feedback
