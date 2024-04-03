from typing import Dict, Union

from rdflib import URIRef

from bob.properties.states import (
    OnOffCommand,
    OnOffStatus,
    OpenCloseCommand,
    OpenCloseStatus,
)
from bob.property import ActuatableProperty

from ...connections.air import (
    AirBidirectionalConnectionPoint,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    CompressedAirConnectionPoint,
    CompressedAirInletConnectionPoint,
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
from ...connections.mechanical import MechanicalCoupling, MechanicalInletConnectionPoint
from ...core import BOB, P223, S223, Equipment, PropertyReference, System, logging
from ...producer import AnalogInput, AnalogOutput
from ...properties import Nm, Percent, PercentCommand
from ...template import template_update, configure_relations

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB

class Damper(Equipment):
    _class_iri = S223.Damper
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.info(f"Fan.__init__ {_config} {kwargs}")
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)