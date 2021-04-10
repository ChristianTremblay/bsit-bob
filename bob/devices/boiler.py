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
from ..signal import AnalogIn

__namespace__ = s223


class HotWaterBoiler(Device):
    hotWaterSupply: HotWaterInletConnectionPoint
    hotWaterReturn: HotWaterOutletConnectionPoint
