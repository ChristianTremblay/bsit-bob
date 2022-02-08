from typing import Any

from ...connections.naturalgas import NaturalGasInletConnectionPoint

from ...connections.electricity import ElectricalInletConnectionPoint

from ...core import s223_proposal, Device


from ...connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)
from ...connections.water import (
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
)
from ...signal import AnalogIn

__namespace__ = s223_proposal


class HotWaterBoiler(Device):
    node_type = s223_proposal.Boiler
    hotWaterSupply: HotWaterInletConnectionPoint
    hotWaterReturn: HotWaterOutletConnectionPoint


class ElectricalHotWaterBoiler(HotWaterBoiler):
    node_type = s223_proposal.Boiler
    electricalInlet: ElectricalInletConnectionPoint


class NaturalGasHotWaterBoiler(HotWaterBoiler):
    node_type = s223_proposal.Boiler
    electricalInlet: ElectricalInletConnectionPoint
    naturalGasInlet: NaturalGasInletConnectionPoint
    combustionAirInlet: AirInletConnectionPoint
    combustionAirOutlet: AirOutletConnectionPoint
