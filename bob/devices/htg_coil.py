from typing import Any

from ..core import (
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
from ..connections.water import (
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    HotWaterInletSystemConnectionPoint,
    HotWaterOutletSystemConnectionPoint,
)
from ..connections.electricity import (
    PowerInletConnectionPoint,
    PowerOutletConnectionPoint,
)

from ..signal import AnalogIn

__namespace__ = s223


class HotWaterCoil(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    hotWaterInlet: HotWaterInletConnectionPoint
    hotWaterOutlet: HotWaterOutletConnectionPoint


# Electrical Coil
class ElectricalCoil(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    powerInlet: PowerInletConnectionPoint
