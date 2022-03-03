from typing import Any

from ...connections.naturalgas import NaturalGasInletConnectionPoint

from ...connections.electricity import ElectricalInletConnectionPoint

from ...core import s223, p223, Device


from ...connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)
from ...connections.water import (
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    CondensedWaterInletConnectionPoint,
    CondensedWaterOutletConnectionPoint,
    WaterOutletConnectionPoint,
    WaterInletConnectionPoint,
)
from ...signal import AnalogIn

__namespace__ = p223


class Chiller(Device):
    node_type = p223.Chiller
    chilledWaterLeaving: ChilledWaterOutletConnectionPoint
    chilledWaterEntering: ChilledWaterInletConnectionPoint
    condensedWaterLeaving: CondensedWaterOutletConnectionPoint
    condensedWaterEntering: CondensedWaterInletConnectionPoint
    powerInlet: ElectricalInletConnectionPoint


class AgnosticChiller(Device):
    node_type = p223.Chiller
    chilledWaterLeaving: WaterOutletConnectionPoint
    chilledWaterEntering: WaterInletConnectionPoint
    condensedWaterLeaving: WaterOutletConnectionPoint
    condensedWaterEntering: WaterInletConnectionPoint
    powerInlet: ElectricalInletConnectionPoint
