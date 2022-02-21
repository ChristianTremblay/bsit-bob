from typing import Any

from rdflib import URIRef
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

# ISSUE
# Technically, valve are manual, electrical, pneumatic... should we define
# all classes or find a way to make it ?


class WaterValve(Device):
    node_type: URIRef = s223.Valve
    waterInlet: WaterInletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint
    position = AnalogIn


class HotWaterValve(Device):
    node_type: URIRef = s223.Valve
    hotWaterInlet: HotWaterInletConnectionPoint
    hotWaterOutlet: HotWaterOutletConnectionPoint
    position = AnalogIn


class ChilledWaterValve(Device):
    node_type: URIRef = s223.Valve
    chilledWaterInlet: ChilledWaterInletConnectionPoint
    chilledWaterOutlet: ChilledWaterOutletConnectionPoint
    position = AnalogIn


class NaturalGasValve(Device):
    node_type: URIRef = s223.Valve
    naturalGasInlet: NaturalGasInletConnectionPoint
    naturalGasOutlet: NaturalGasOutletConnectionPoint
    position = AnalogIn


class PneumaticValve(Device):
    node_type: URIRef = s223.Valve
    compressedAirInlet: CompressedAirConnectionPoint
    position = AnalogIn
