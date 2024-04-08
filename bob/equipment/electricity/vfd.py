from typing import Dict

from rdflib import URIRef

from ...equipment.control.controller import Controller
from ...equipment.electricity import _VFD
from ...producer import Function, FunctionInput, FunctionOutput
from ...producer.causality import Causality
from ...properties.electricity import Frequency, Volts
from ...sensor.electricity import CurrentSensor, VoltageSensor
from ...sensor.motion import PositionSensor

from ...connections.controlsignal import (
    ModulationSignalInletConnectionPoint,
    OnOffSignalOutletConnectionPoint,
)
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
)
from ...connections.network import (
    EthernetBidirectionalConnectionPoint,
    RS485BidirectionalConnectionPoint,
)
from ...core import (
    BOB,
    P223,
    S223,
    SCRATCH,
    ConnectionPoint,
    Equipment,
    Property,
    PropertyReference,
    logging,
)
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
from ...template import template_update, configure_relations

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = SCRATCH


vfd_template = {
    "cp": {
        "electricalInlet": ElectricalInletConnectionPoint,
        "electricalOutlet": ElectricalOutletConnectionPoint,
    },
    "properties": {
    },
    "parts": {
    },
}


class VFD(_VFD):
    _class_iri: URIRef = S223.VariableFrequencyDrive

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(vfd_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"VFD.__init__ {_config} {kwargs}")
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)

       