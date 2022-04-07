from typing import Any

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ModulationSignalInletConnectionPoint,
    OnOffSignalOutletConnectionPoint,
)
from ...connections.naturalgas import NaturalGasInletConnectionPoint
from ...connections.water import (
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    CondensedWaterInletConnectionPoint,
    CondensedWaterOutletConnectionPoint,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...core import Device, p223, s223
from ...properties import OnOffCommand, OnOffStatus, Percent, Temperature
from ...signal import AnalogIn

__namespace__ = p223


class Chiller(Device):
    node_type = p223.Chiller
    # refrigerant
    # manufacturer
    waterResetInlet: ModulationSignalInletConnectionPoint
    alarmOutlet: OnOffSignalOutletConnectionPoint
    capacityLimitInlet: ModulationSignalInletConnectionPoint

    hasWaterReset: Percent
    hasCapacityLimit: Percent
    hasOnOffStatus: OnOffStatus
    hasOnOffCommand: OnOffCommand

    def __init__(self, **kwargs):
        self.electricalInlet = kwargs.pop(
            "electricalInlet", ChilledWaterOutletConnectionPoint
        )
        self.chilledWaterLeaving = kwargs.pop(
            "chilledWaterLeaving", ChilledWaterOutletConnectionPoint
        )
        self.chilledWaterEntering = kwargs.pop(
            "chilledWaterEntering", ChilledWaterInletConnectionPoint
        )
        self.condensedWaterLeaving = kwargs.pop(
            "condensedWaterLeaving", CondensedWaterOutletConnectionPoint
        )
        self.condensedWaterEntering = kwargs.pop(
            "condensedWaterEntering", CondensedWaterInletConnectionPoint
        )
        super().__init__(**kwargs)


class AgnosticChiller(Device):
    node_type = p223.Chiller
    chilledWaterLeaving: WaterOutletConnectionPoint
    chilledWaterEntering: WaterInletConnectionPoint
    condensedWaterLeaving: WaterOutletConnectionPoint
    condensedWaterEntering: WaterInletConnectionPoint
    powerInlet: ElectricalInletConnectionPoint
