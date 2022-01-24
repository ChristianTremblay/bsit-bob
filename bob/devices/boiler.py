from typing import Any

from ..connections.naturalgas import NaturalGasInletConnectionPoint

from ..connections.electricity import ElectricalInletConnectionPoint

from ..core import (
    s223,
)

from ..node import Device

from ..connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)
from ..connections.water import (
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
)
from ..signal import AnalogIn

__namespace__ = s223


class HotWaterBoiler(Device):
    hotWaterSupply: HotWaterInletConnectionPoint
    hotWaterReturn: HotWaterOutletConnectionPoint


class ElectricalHotWaterBoiler(HotWaterBoiler):
    electricalInlet: ElectricalInletConnectionPoint


class NaturalGasHotWaterBoiler(HotWaterBoiler):
    electricalInlet: ElectricalInletConnectionPoint
    naturalGasInlet: NaturalGasInletConnectionPoint
    combustionAirInlet: AirInletConnectionPoint
    combustionAirOutlet: AirOutletConnectionPoint
