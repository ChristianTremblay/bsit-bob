import logging
from typing import Any, Dict

from rdflib import URIRef

from ...connections.air import (
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from ...connections.electricity import (
    Electricity_600VLL_3Ph_60HzSystemInletConnectionPoint,
)
from ...core import BOB, P223, S223, Equipment, System, template_update

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB

ahu_template = {
    "params": {},
    "sensors": {},
    "equipment": {},
}

fan_coil_template = {
    "params": {},
    "sensors": {},
    "equipment": {},
}


class AirHandlingUnit(System):
    _class_iri = P223.AirHandlingUnit
    outsideAirInlet: AirInletSystemConnectionPoint
    returnAirInlet: AirInletSystemConnectionPoint
    supplyAirOutlet: AirOutletSystemConnectionPoint
    exhaustAirOutlet: AirOutletSystemConnectionPoint
    electricalInlet: Electricity_600VLL_3Ph_60HzSystemInletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(ahu_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"AirHandlingUnit.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)


class FanCoil(System):
    _class_iri = P223.Fancoil
    returnAirInlet: AirInletSystemConnectionPoint
    supplyAirOutlet: AirOutletSystemConnectionPoint
    exhaustAirOutlet: AirOutletSystemConnectionPoint
    electricalInlet: Electricity_600VLL_3Ph_60HzSystemInletConnectionPoint

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        _config = template_update(fan_coil_template, config)
        kwargs = {**_config.get("params", {}), **kwargs}
        _log.debug(f"FanCoil.__init__ {_config} {kwargs}")
        super().__init__(config, **kwargs)
