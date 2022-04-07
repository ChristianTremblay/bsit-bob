from typing import Any

from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)
from ...core import Device, p223, s223
from ...signal import AnalogIn

__namespace__ = p223

# SCR
class SCR(Device):
    # takes 600V (or 347V) in and use triacs to modulate
    # power given to electrical coil
    electricalInlet: ElectricalInletConnectionPoint
    electricalOutlet: ElectricalOutletConnectionPoint
    modulation = AnalogIn
