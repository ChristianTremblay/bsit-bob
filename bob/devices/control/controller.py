from typing import Dict

from rdflib import URIRef
from bob.functions import FunctionBlock

from bob.properties import Nm, Percent, PercentCommand
from bob.properties.states import OnOffCommand, OnOffStatus

from ...connections.electricity import (
    ModulationSignalInletConnectionPoint,
    ModulationSignalOutletConnectionPoint,
    OnOffSignalInletConnectionPoint,
    OnOffSignalOutletConnectionPoint,
    RS485BidirectionalConnectionPoint,
    Electricity_24V_60HzInletConnectionPoint,
)

from ...core import (
    Device,
    Property,
    PropertyReference,
    logging,
    BOB,
    P223,
    S223,
    template_update,
)

_namespace = P223

# Controller
analogInput = ModulationSignalInletConnectionPoint
analogInput._class_iri = P223.AnalogInput
analogOutput = ModulationSignalOutletConnectionPoint
analogOutput._class_iri = P223.AnalogOutput
binaryInput = OnOffSignalInletConnectionPoint
binaryInput._class_iri = P223.BinaryInput
binaryOutput = OnOffSignalOutletConnectionPoint
binaryOutput._class_iri = P223.BinaryOutput
bacnet_mstp = RS485BidirectionalConnectionPoint

controller_template = {
    "cp": {
        "electricalInlet": Electricity_24V_60HzInletConnectionPoint,
        "zone_temperature_sensor": analogInput,
        "airflow_sensor": analogInput,
        "damper_output": analogOutput,
    },
    "properties": {},
}


class Controller(Device):
    """
    A controller executes function blocks and connect to other devices
    through different connection points (AI, AO, BI, BO)
    """

    _class_iri: URIRef = S223.Controller
    # electricalInlet: Electricity_24V_60HzInletConnectionPoint
    # executes: FunctionBlock

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(controller_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        logging.debug(f"Controller.__init__ {_config} {kwargs}")

        super().__init__(_config, **kwargs)
