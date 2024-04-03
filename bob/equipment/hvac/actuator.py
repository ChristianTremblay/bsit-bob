from typing import Dict, Union
import logging
from rdflib import URIRef

from ...connections.mechanical import MechanicalOutletConnectionPoint
from ...enum import OpenCloseEnum
from ...producer import Producer, ProducerInput, ProducerOutput
from ...producer.causality import Causality
from ...properties import Nm, Percent, PercentCommand
from ...properties.states import OnOffCommand, OnOffStatus
from ...sensor.motion import PositionSensor
from ...sensor.sensor import Sensor

from ...connections.air import (
    AirBidirectionalConnectionPoint,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    CompressedAirConnectionPoint,
    CompressedAirInletConnectionPoint,
    CompressedAirOutletConnectionPoint,
)
from ...connections.controlsignal import (
    ModulationSignalInletConnectionPoint,
    ModulationSignalOutletConnectionPoint,
    OnOffSignalInletConnectionPoint,
    OnOffSignalOutletConnectionPoint,
)
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    Electricity_24VLN_1Ph_60HzInletConnectionPoint,
    Electricity_120VLN_1Ph_60HzInletConnectionPoint,
)
from ...connections.light import (
    LightOutletConnectionPoint,
    LightVisibleOutletConnectionPoint,
)
from ...core import BOB, P223, S223, Equipment, Property, PropertyReference
from ...template import template_update, configure_relations
from .. import _Actuator

# logging
_log = logging.getLogger(__name__)

_namespace = BOB

"""
 
__|___|__|___|___|__                                                                                  
|     Actuator     |------------s223:hasProperty--------(actuates) -> A                                   
|  s223:Equipment  |------------s223:hasProperty--------(commandedByProperty) -> B
|                  |
|                  |
|__________________|

"""

class Actuator(Equipment):
    _class_iri = S223.Actuator
    actuates: PropertyReference
    commandedByProperty: PropertyReference


    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.info(f"Actuator.__init__ {_config} {kwargs}")
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)