from typing import Dict

from rdflib import URIRef

from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
    Electricity_575V_60HzInletConnectionPoint,
    Electricity_575V_60HzOutletConnectionPoint,
)
from ...core import ConnectionPoint, Device, Property, bob, p223, s223
from ...properties import (
    HP,
    RPM,
    Amps,
    ElectricPowerkW,
    NormalAlarmStatus,
    OnOffCommand,
    OnOffStatus,
    Percent,
    PercentCommand,
    PowerFactor,
    Temperature,
)

_namespace = bob

vfd_template = {
    "cp": {
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
        "electricalOutlet": Electricity_575V_60HzOutletConnectionPoint,
    },
    "properties": {
        ("amps", Amps): {},
        ("hp", HP): {},
        ("kW", ElectricPowerkW): {},
        ("speed_reference", PercentCommand): {},
        ("rpm", RPM): {},
        ("motor_temp", Temperature): {},
        ("drive_running", OnOffStatus): {},
        ("run_command", OnOffCommand): {},
        ("alarm_status", NormalAlarmStatus): {},
    },
}


class VFD(Device):
    _class_iri: URIRef = s223.VariableFrequencyDrive

    def __init__(self, config: Dict = vfd_template, **kwargs):
        config["properties"] = config.get("properties", vfd_template["properties"])
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
