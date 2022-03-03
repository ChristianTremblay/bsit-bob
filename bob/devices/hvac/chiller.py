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
)
from ...signal import AnalogIn

__namespace__ = p223


class Chiller(Device):
    node_type = p223.Boiler
    chilledWaterLeaving: ChilledWaterOutletConnectionPoint
    chilledWaterEntering: ChilledWaterInletConnectionPoint
    condensedWaterLeaving: CondensedWaterOutletConnectionPoint
    condensedWaterEntering: CondensedWaterInletConnectionPoint
    powerInlet: ElectricalInletConnectionPoint
