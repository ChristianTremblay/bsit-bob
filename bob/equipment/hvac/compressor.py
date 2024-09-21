from typing import Dict

from rdflib import URIRef

from bob.properties.electricity import ElectricPowerkW
from bob.properties.states import NormalAlarmStatus, OnOffCommand, OnOffStatus

from ...connections.air import CompressedAirOutletConnectionPoint
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
)
from ...connections.refrigerant import (
    RefrigerationGasInletConnectionPoint,
    RefrigerationGasOutletConnectionPoint,
)
from ...core import BOB, P223, S223, Equipment, PropertyReference
from ...enum import (  # , R134a, R404a, R407c, R448a, R449a, R452a, R454b, R507a
    R22,
    R32,
    R410a,
    RefrigerationGas,
)

_namespace = BOB

compressor_template = {
    "cp": {"electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint},
    "properties": {
        ("kW", ElectricPowerkW): {},
    },
}


class AirCompressor(Equipment):
    _class_iri: URIRef = S223.Compressor
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


class RefrigeartionGasCompressor(Equipment):
    _class_iri: URIRef = S223.Compressor
    returnPort: RefrigerationGasInletConnectionPoint
    dischargePort: RefrigerationGasOutletConnectionPoint

    onOffStatus: OnOffStatus
    alarmStatus: NormalAlarmStatus
    onOffCommand: OnOffCommand

    # This will come from a sensor, but accessible from here
    dischargePressure: PropertyReference
    succionPressure: PropertyReference

    def __init__(self, config: Dict = compressor_template, **kwargs):
        config["properties"] = config.get(
            "properties", compressor_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)

    def set_gas_type(self, gas: RefrigerationGas):
        self.returnPort.hasMedium = gas
        self.dischargePort.hasMedium = gas
