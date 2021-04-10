from typing import Any

from .core import (
    s223,
    Substance,
    Connection,
    Device,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    System,
    SystemConnectionPoint,
    InletSystemConnectionPoint,
    OutletSystemConnectionPoint,
)
from .connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)

from .connections.electricity import (
    PowerInletConnectionPoint,
    PowerOutletConnectionPoint,
)


from .signal import AnalogIn

__namespace__ = s223

# SCR
class SCR(Device):
    # takes 600V (or 347V) in and use triacs to modulate 
    # power given to electrical coil
    powerInlet: PowerInletConnectionPoint
    powerOutlet: PowerOutletConnectionPoint
    modulation = AnalogIn

#class Stages(Device):
#    # Each stages have % of power
#    PowerInlet: PowerInletConnectionPoint
#    PowerOutlet: PowerOutletConnectionPoint
#    modulation = AnalogIn

# Electrical Coil
class ElectricalCoil(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    powerInlet: PowerInletConnectionPoint


class ElectricalCoilWithSCR(System):
    """
    This is an example of a hot water coil that contains its valve as a
    subsystem and makes the valve position available as its own connection
    point.
    """

    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    powerInlet: PowerInletConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a electrical heating coil
        self.electrical_heating_coil = ElectricalCoil(label=self.label + ".elechtg_coil")
        self.airInlet.mapsTo = self.electrical_heating_coil.airInlet
        self.airOutlet.mapsTo = self.electrical_heating_coil.airOutlet

        # create a SCR to modulate the coil
        self.scr = SCR(label=self.label + ".elechtg_scr")
        self.powerInlet.mapsTo = self.scr.powerInlet
        self.scr.powerOutlet.mapsTo = self.electrical_heating_coil.powerInlet
        self.scr >> self.electrical_heating_coil

        # reference the SCR modulation command
        self.scr_modulation = self.scr.modulation
