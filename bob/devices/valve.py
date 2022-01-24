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
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
)
from ..signal import AnalogIn

__namespace__ = s223


class HotWaterValve(Device):
    hotWaterInlet: HotWaterInletConnectionPoint
    hotWaterOutlet: HotWaterOutletConnectionPoint
    position = AnalogIn


class ChilledWaterValve(Device):
    chilledWaterInlet: ChilledWaterInletConnectionPoint
    chilledWaterOutlet: ChilledWaterOutletConnectionPoint
    position = AnalogIn
