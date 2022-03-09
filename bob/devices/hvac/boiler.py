from typing import Any

from ...connections.naturalgas import NaturalGasInletConnectionPoint

from ...connections.electricity import ElectricalInletConnectionPoint

from ...core import s223, p223, Device


from ...connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)
from ...connections.water import (
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
)
from ...signal import AnalogIn

__namespace__ = p223


class HotWaterBoiler(Device):
    node_type = p223.Boiler
    hotWaterLeaving: HotWaterInletConnectionPoint
    hotWaterEntering: HotWaterOutletConnectionPoint


class ElectricalHotWaterBoiler(HotWaterBoiler):
    node_type = p223.Boiler
    electricalInlet: ElectricalInletConnectionPoint


class NaturalGasHotWaterBoiler(HotWaterBoiler):
    node_type = p223.Boiler
    electricalInlet: ElectricalInletConnectionPoint
    naturalGasInlet: NaturalGasInletConnectionPoint
    combustionAirInlet: AirInletConnectionPoint
    combustionAirOutlet: AirOutletConnectionPoint
