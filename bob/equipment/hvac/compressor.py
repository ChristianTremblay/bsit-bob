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
from ...core import BOB, P223, S223, Equipment, PropertyReference

_namespace = BOB

compressor_template = {
    "cp": {"electricalInlet": Electricity_575V_60HzInletConnectionPoint},
    "properties": {
        ("kW", ElectricPowerkW): {},
    },
}


class AirCompressor(Equipment):
    _class_iri: URIRef = P223.AirCompressor
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
