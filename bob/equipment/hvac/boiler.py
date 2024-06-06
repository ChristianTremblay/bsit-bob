from typing import Any

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...connections.electricity import ElectricalInletConnectionPoint
from ...connections.naturalgas import NaturalGasInletConnectionPoint
from ...connections.liquid import (
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...core import BOB, P223, S223, Equipment

_namespace = BOB


class HotWaterBoiler(Equipment):
    _class_iri = S223.Boiler
    hotWaterLeaving: HotWaterOutletConnectionPoint
    hotWaterEntering: HotWaterInletConnectionPoint


class ElectricalHotWaterBoiler(HotWaterBoiler):
    _class_iri = S223.Boiler
    electricalInlet: ElectricalInletConnectionPoint


class NaturalGasHotWaterBoiler(HotWaterBoiler):
    _class_iri = S223.Boiler
    electricalInlet: ElectricalInletConnectionPoint
    naturalGasInlet: NaturalGasInletConnectionPoint
    combustionAirInlet: AirInletConnectionPoint
    combustionAirOutlet: AirOutletConnectionPoint
    condensedWaterOutlet: WaterOutletConnectionPoint
