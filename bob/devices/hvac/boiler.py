from typing import Any

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...connections.electricity import ElectricalInletConnectionPoint
from ...connections.naturalgas import NaturalGasInletConnectionPoint
from ...connections.water import (
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...core import Device, p223, s223

_namespace = s223


class HotWaterBoiler(Device):
    node_type = s223.Boiler
    hotWaterLeaving: HotWaterInletConnectionPoint
    hotWaterEntering: HotWaterOutletConnectionPoint


class ElectricalHotWaterBoiler(HotWaterBoiler):
    node_type = s223.Boiler
    electricalInlet: ElectricalInletConnectionPoint


class NaturalGasHotWaterBoiler(HotWaterBoiler):
    node_type = s223.Boiler
    electricalInlet: ElectricalInletConnectionPoint
    naturalGasInlet: NaturalGasInletConnectionPoint
    combustionAirInlet: AirInletConnectionPoint
    combustionAirOutlet: AirOutletConnectionPoint
    condensedWaterOutlet: WaterOutletConnectionPoint
