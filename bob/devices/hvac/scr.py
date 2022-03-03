from typing import Any

from ...core import s223, p223
from ...core import Device

from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)


from ...signal import AnalogIn

__namespace__ = p223

# SCR
class SCR(Device):
    # takes 600V (or 347V) in and use triacs to modulate
    # power given to electrical coil
    electricalInlet: ElectricalInletConnectionPoint
    electricalOutlet: ElectricalOutletConnectionPoint
    modulation = AnalogIn
