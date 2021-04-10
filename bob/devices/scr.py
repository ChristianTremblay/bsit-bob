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
from ..connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)

from ..connections.electricity import (
    PowerInletConnectionPoint,
    PowerOutletConnectionPoint,
)


from ..signal import AnalogIn

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

