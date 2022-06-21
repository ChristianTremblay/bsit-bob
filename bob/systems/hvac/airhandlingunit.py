import logging
from typing import Any, Dict

from attr import set_run_validators
from rdflib import URIRef

from ...connections.air import (
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from ...connections.electricity import Electricity_575V_60HzSystemInletConnectionPoint
from ...core import Device, System, BOB, P223, S223

_namespace = BOB

ahu_template = {
    "params": {"label": "Name", "comment": "Description"},
    "sensors": {},
    "devices": {("sub_device1_label", Device): {"comment": "SubDev comment"}},
}


class AirHandlingUnit(System):
    _class_iri = P223.AirHandlingUnit
    outsideAirInlet: AirInletSystemConnectionPoint
    returnAirInlet: AirInletSystemConnectionPoint
    supplyAirOutlet: AirOutletSystemConnectionPoint
    exhaustAirOutlet: AirOutletSystemConnectionPoint
    electricalInlet: Electricity_575V_60HzSystemInletConnectionPoint

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class FanCoil(System):
    _class_iri = P223.Fancoil
    returnAirInlet: AirInletSystemConnectionPoint
    supplyAirOutlet: AirOutletSystemConnectionPoint
    exhaustAirOutlet: AirOutletSystemConnectionPoint
    electricalInlet: Electricity_575V_60HzSystemInletConnectionPoint

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
