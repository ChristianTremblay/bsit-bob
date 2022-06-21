from typing import Dict

from rdflib import URIRef

from bob.properties import Nm, Percent, PercentCommand
from bob.properties.states import OnOffCommand, OnOffStatus

from ...connections.air import (
    AirBidirectionalConnectionPoint,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    CompressedAirConnectionPoint,
    CompressedAirInletConnectionPoint,
    CompressedAirOutletConnectionPoint,
)
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    Electricity_24V_60HzInletConnectionPoint,
    Electricity_120V_60HzInletConnectionPoint,
)
from ...connections.light import (
    LightOutletConnectionPoint,
    LightVisibleOutletConnectionPoint,
)
from ...core import (
    Device,
    Property,
    PropertyReference,
    BOB,
    P223,
    S223,
    template_update,
)
from . import _Actuator

_namespace = BOB

# ACTUATORS


class Actuator(_Actuator):
    _class_iri = S223.Actuator
    command: PercentCommand
    actuatesProperty: Property
    feedback: Percent
    torque: Nm

    def __init__(self, config: Dict = {}, **kwargs):
        config["properties"] = config.get("properties", {})
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class ProportionalActuator(Actuator):
    _class_iri = S223.Actuator
    command: PercentCommand
    actuatesProperty: PercentCommand
    feedback: Percent

    def __init__(self, config: Dict = {}, **kwargs):
        config["properties"] = config.get("properties", {})
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class OnOffActuator(Actuator):
    _class_iri = S223.Actuator
    command: OnOffCommand
    actuatesProperty: OnOffCommand
    feedbackOpen: OnOffStatus
    feedbackClose: OnOffStatus

    def __init__(self, config: Dict = {}, **kwargs):
        config["properties"] = config.get("properties", {})
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


ElectricalProportionalActuator_template = {
    "cp": {"electricalInlet": Electricity_24V_60HzInletConnectionPoint},
    "properties": {
        ("actuatesProperty", PercentCommand): {},
        ("command", PercentCommand): {},
        ("feedback", Percent): {},
        ("torque", Nm): {},
    },
}


ElectricalOnOffActuator_template = {
    "cp": {"electricalInlet": Electricity_24V_60HzInletConnectionPoint},
    "properties": {
        ("actuatesProperty", OnOffCommand): {},
        ("command", OnOffCommand): {},
        ("feedbackOpen", OnOffStatus): {},
        ("feedbackClose", OnOffStatus): {},
        ("torque", Nm): {},
    },
}


class ElectricalProportionalActuator(ProportionalActuator):
    _class_iri = S223.Actuator

    def __init__(
        self, config: Dict = ElectricalProportionalActuator_template, **kwargs
    ):
        _config = template_update(ElectricalProportionalActuator_template, config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


class ElectricalOnOffActuator(OnOffActuator):
    _class_iri = S223.Actuator

    def __init__(self, config: Dict = ElectricalOnOffActuator_template, **kwargs):
        _config = template_update(ElectricalOnOffActuator_template, config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


PneumaticProportionalActuator_template = {
    "cp": {},
    "properties": {
        ("actuatesProperty", PercentCommand): {},
        ("command", PercentCommand): {},
        ("feedback", Percent): {},
        ("torque", Nm): {},
    },
}

PneumaticOnOffActuator_template = {
    "cp": {},
    "properties": {
        ("actuatesProperty", OnOffCommand): {},
        ("command", OnOffCommand): {},
        ("feedbackOpen", OnOffStatus): {},
        ("feedbackClose", OnOffStatus): {},
        ("torque", Nm): {},
    },
}


class PneumaticProportionalActuator(ProportionalActuator):
    _class_iri = S223.Actuator
    compressedAirInlet: CompressedAirInletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(PneumaticProportionalActuator_template, config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


class PneumaticOnOffActuator(OnOffActuator):
    _class_iri = S223.Actuator
    compressedAirInlet: CompressedAirInletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = PneumaticOnOffActuator_template
        if config:
            _config.update(config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
