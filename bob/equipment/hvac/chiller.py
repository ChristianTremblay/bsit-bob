from typing import Dict

from bob.properties.electricity import ElectricPowerkW
from bob.properties.states import NormalAlarmStatus

from ...connections.electricity import (
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
)
from ...connections.controlsignal import (
    ModulationSignalInletConnectionPoint,
    OnOffSignalOutletConnectionPoint,
)
from ...connections.liquid import (
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    CondenserInletConnectionPoint,
    CondenserOutletConnectionPoint,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...core import BOB, S223, Equipment
from ...properties import OnOffCommand, OnOffStatus, Percent
from ...template import template_update, configure_relations

_namespace = BOB

class Chiller(Equipment):
    _class_iri = S223.Chiller
    chilledWaterEntering: WaterInletConnectionPoint
    chilledWaterLeaving: WaterOutletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
