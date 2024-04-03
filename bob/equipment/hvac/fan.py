import logging
from typing import Dict

from rdflib import URIRef

from ...equipment.electricity.vfd import VFD
from ...properties.flow import Flow
from ...properties.ratio import Percent, PercentCommand

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
)
from ...core import (
    BOB,
    QUANTITYKIND,
    S223,
    UNIT,
    ConnectionPoint,
    Equipment,
    PropertyReference,
)
from ...properties import HP, RPM, Amps, ElectricPowerkW, PowerFactor, Pressure
from ...properties.states import OnOffCommand, OnOffStatus
from ...property import QuantifiableObservableProperty
from ...template import configure_relations, template_update
from ..electricity.starter import MotorStarter
from ..electricity.vfd import VFD

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB


fan_template = {
    "cp": {
        "electricalInlet": ElectricalInletConnectionPoint
    }
}

class Fan(Equipment):
    """
    A fan is composed of a blower and an electrical motor
    """

    _class_iri: URIRef = S223.Fan
    #electricalInlet: ElectricalInletConnectionPoint # needs to be in a template so other templates can override it.
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(fan_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.info(f"Fan.__init__ {_config} {kwargs}")
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)

