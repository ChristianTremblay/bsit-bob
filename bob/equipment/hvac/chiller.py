from typing import Any, Dict

from bob.properties.electricity import ElectricPowerkW
from bob.properties.states import NormalAlarmStatus

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
)
from ...connections.controlsignal import (
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
from ...core import BOB, P223, S223, Equipment
from ...properties import OnOffCommand, OnOffStatus, Percent, Temperature

_namespace = BOB

chiller_template = {
    "cp": {"electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint},
    "properties": {
        ("kW", ElectricPowerkW): {},
    },
}


class Chiller(Equipment):
    _class_iri = S223.Chiller
    chilledWaterEntering: ChilledWaterInletConnectionPoint
    chilledWaterLeaving: ChilledWaterOutletConnectionPoint
    condensedWaterEntering: CondensedWaterInletConnectionPoint
    condensedWaterLeaving: CondensedWaterOutletConnectionPoint

    # refrigerant
    # manufacturer
    setpointResetInlet: ModulationSignalInletConnectionPoint
    alarmOutlet: OnOffSignalOutletConnectionPoint
    capacityLimitInlet: ModulationSignalInletConnectionPoint

    setpointReset: Percent
    capacityLimit: Percent
    onOffStatus: OnOffStatus
    alarmStatus: NormalAlarmStatus
    onOffCommand: OnOffCommand

    def __init__(self, config: Dict = chiller_template, **kwargs):
        config["properties"] = config.get("properties", chiller_template["properties"])
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class AgnosticChiller(Equipment):
    _class_iri = S223.Chiller
    chilledWaterLeaving: WaterOutletConnectionPoint
    chilledWaterEntering: WaterInletConnectionPoint
    condensedWaterLeaving: WaterOutletConnectionPoint
    condensedWaterEntering: WaterInletConnectionPoint

    # refrigerant
    # manufacturer
    setpointResetInlet: ModulationSignalInletConnectionPoint
    alarmOutlet: OnOffSignalOutletConnectionPoint
    capacityLimitInlet: ModulationSignalInletConnectionPoint

    setpointReset: Percent
    capacityLimit: Percent
    onOffStatus: OnOffStatus
    alarmStatus: NormalAlarmStatus
    onOffCommand: OnOffCommand

    def __init__(self, config: Dict = chiller_template, **kwargs):
        config["properties"] = config.get("properties", chiller_template["properties"])
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
