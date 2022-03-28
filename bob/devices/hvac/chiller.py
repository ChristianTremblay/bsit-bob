from typing import Any

from ...connections.naturalgas import NaturalGasInletConnectionPoint

from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ModulationSignalInletConnectionPoint,
    OnOffSignalOutletConnectionPoint,
)

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

from ...properties import OnOffStatus, OnOffCommand, Percent, Temperature

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
