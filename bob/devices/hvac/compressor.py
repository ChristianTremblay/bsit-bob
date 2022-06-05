from typing import Dict

from rdflib import URIRef

from bob.properties.electricity import ElectricPowerkW
from bob.properties.states import NormalAlarmStatus, OnOffCommand, OnOffStatus

from ...connections.air import CompressedAirOutletConnectionPoint
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
    Electricity_575V_60HzInletConnectionPoint,
)
from ...core import Device, PropertyReference, p223, s223

_namespace = p223

compressor_template = {
    "cp": {"electricalInlet": Electricity_575V_60HzInletConnectionPoint},
    "properties": {
        ("kW", ElectricPowerkW): {},
    },
}


class AirCompressor(Device):
    _class_iri: URIRef = p223.AirCompressor
    compressedAirOutlet: CompressedAirOutletConnectionPoint

    onOffStatus: OnOffStatus
    alarmStatus: NormalAlarmStatus
    onOffCommand: OnOffCommand

    # This will come from a sensor, but accessible from here
    outputPressure: PropertyReference

    def __init__(self, config: Dict = compressor_template, **kwargs):
        config["properties"] = config.get(
            "properties", compressor_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
