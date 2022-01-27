from typing import Any
from bob.connections.air import CompressedAirConnectionPoint

from bob.connections.naturalgas import (
    NaturalGasInletConnectionPoint,
    NaturalGasOutletConnectionPoint,
)

from ...core import s223, Device


from ...connections.water import (
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...signal import AnalogIn

__namespace__ = s223


# Technically, valve are manual, electrical, pneumatic... should we define
# all classes or find a way to make it ?


class WaterValve(Device):
    waterInlet: WaterInletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint
    position = AnalogIn


class HotWaterValve(Device):
    hotWaterInlet: HotWaterInletConnectionPoint
    hotWaterOutlet: HotWaterOutletConnectionPoint
    position = AnalogIn


class ChilledWaterValve(Device):
    chilledWaterInlet: ChilledWaterInletConnectionPoint
    chilledWaterOutlet: ChilledWaterOutletConnectionPoint
    position = AnalogIn


class NaturalGasValve(Device):
    naturalGasInlet: NaturalGasInletConnectionPoint
    naturalGasOutlet: NaturalGasOutletConnectionPoint
    position = AnalogIn


class PneumaticValve(Device):
    compressedAirInlet: CompressedAirConnectionPoint
    position = AnalogIn
