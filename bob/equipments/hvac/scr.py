from typing import Any, Dict

from rdflib import URIRef

from bob.properties import PercentCommand
from bob.properties.electricity import Amps, ElectricPowerkW

from ...connections.electricity import (
    Electricity_575V_60HzInletConnectionPoint,
    Electricity_575V_60HzOutletConnectionPoint,
    ModulationSignalInletConnectionPoint,
)
from ...core import BOB, P223, S223, Equipment

_namespace = BOB

# SCR
SCR_template = {
    "cp": {
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
        "electricalOutlet": Electricity_575V_60HzOutletConnectionPoint,
        "modulationSignal": ModulationSignalInletConnectionPoint,
    },
    "properties": {
        ("modulation", PercentCommand): {},
        ("amps", Amps): {},
        ("kW", ElectricPowerkW): {},
    },
}


class SCR(Equipment):
    # takes 600V (or 347V) in and use triacs to modulate
    # power given to electrical coil
    # a SCR accept 0-10VDC signal to modulate
    _class_iri: URIRef = P223.SCR

    def __init__(self, config: Dict = SCR_template, **kwargs):
        config["properties"] = config.get("properties", SCR_template["properties"])
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
