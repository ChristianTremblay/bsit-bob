from typing import Any

from ..core import (
    s223,
)

from ..node import Device

from ..connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)

from ..connections.water import (
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
)

from ..connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)

from ..signal import AnalogIn

__namespace__ = s223


class ChilledWaterCoil(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    chilledWaterInlet: ChilledWaterInletConnectionPoint
    chilledWaterOutlet: ChilledWaterOutletConnectionPoint


class HotWaterCoil(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    hotWaterInlet: HotWaterInletConnectionPoint
    hotWaterOutlet: HotWaterOutletConnectionPoint


# Electrical Coil
class ElectricalHeatingCoil(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    powerInlet: ElectricalInletConnectionPoint  # can come from a SCR or a contactor...(maybe more than 1 contactor that would give x% of power)
