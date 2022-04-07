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
from ...core import Device, System, p223

__namespace__ = p223

ahu_template = {
    "params": {"label": "Name", "comment": "Description"},
    "sensors": {},
    "devices": {("sub_device1_label", Device): {"comment": "SubDev comment"}},
}


class AirHandlingUnit(System):
    outsideAirInlet: AirInletSystemConnectionPoint
    returnAirInlet: AirInletSystemConnectionPoint
    supplyAirOutlet: AirOutletSystemConnectionPoint
    exhaustAirOutlet: AirOutletSystemConnectionPoint
    electricalInlet: Electricity_575V_60HzSystemInletConnectionPoint

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class FanCoil(System):
    returnAirInlet: AirInletSystemConnectionPoint
    supplyAirOutlet: AirOutletSystemConnectionPoint
    exhaustAirOutlet: AirOutletSystemConnectionPoint
    electricalInlet: Electricity_575V_60HzSystemInletConnectionPoint

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
