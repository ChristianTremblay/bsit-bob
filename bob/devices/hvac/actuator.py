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
from ...core import Device, Property, PropertyReference, p223, s223

_namespace = s223

# ACTUATORS


class Actuator(Device):
    _class_iri = s223.Actuator
    command: PercentCommand
    actuatesProperty: Property
    feedback: Percent
    torque: Nm

    def __init__(self, config: Dict = {}, **kwargs):
        config["properties"] = config.get("properties", {})
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class ProportionalActuator(Actuator):
    _class_iri = s223.Actuator
    command: PercentCommand
    actuatesProperty: Property
    feedback: Percent

    def __init__(self, config: Dict = {}, **kwargs):
        config["properties"] = config.get("properties", {})
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class OnOffActuator(Actuator):
    _class_iri = s223.Actuator
    command: OnOffCommand
    actuatesProperty: Property
    feedbackOpen: OnOffStatus
    feedbackClose: OnOffStatus

    def __init__(self, config: Dict = {}, **kwargs):
        config["properties"] = config.get("properties", {})
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


ElectricalProportionalActuator_template = {
    "cp": {"electricalInlet": Electricity_24V_60HzInletConnectionPoint},
    "properties": {
        ("command", PercentCommand): {},
        ("feedback", Percent): {},
        ("torque", Nm): {},
    },
}


ElectricalOnOffActuator_template = {
    "cp": {"electricalInlet": Electricity_24V_60HzInletConnectionPoint},
    "properties": {
        ("command", OnOffCommand): {},
        ("feedbackOpen", OnOffStatus): {},
        ("feedbackClose", OnOffStatus): {},
        ("torque", Nm): {},
    },
}


class ElectricalProportionalActuator(ProportionalActuator):
    _class_iri = s223.Actuator

    def __init__(
        self, config: Dict = ElectricalProportionalActuator_template, **kwargs
    ):
        config["properties"] = config.get(
            "properties", ElectricalProportionalActuator_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class ElectricalOnOffActuator(OnOffActuator):
    _class_iri = s223.Actuator

    def __init__(self, config: Dict = ElectricalOnOffActuator_template, **kwargs):
        config["properties"] = config.get(
            "properties", ElectricalOnOffActuator_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


PneumaticProportionalActuator_template = {
    "cp": {},
    "properties": {
        ("command", PercentCommand): {},
        ("feedback", Percent): {},
        ("torque", Nm): {},
    },
}

PneumaticOnOffActuator_template = {
    "cp": {},
    "properties": {
        ("command", OnOffCommand): {},
        ("feedbackOpen", OnOffStatus): {},
        ("feedbackClose", OnOffStatus): {},
        ("torque", Nm): {},
    },
}


class PneumaticProportionalActuator(ProportionalActuator):
    _class_iri = s223.Actuator
    compressedAirInlet: CompressedAirInletConnectionPoint

    def __init__(self, config: Dict = PneumaticProportionalActuator_template, **kwargs):
        config["properties"] = config.get(
            "properties", PneumaticProportionalActuator_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class PneumaticOnOffActuator(OnOffActuator):
    _class_iri = s223.Actuator
    compressedAirInlet: CompressedAirInletConnectionPoint

    def __init__(self, config: Dict = PneumaticOnOffActuator_template, **kwargs):
        config["properties"] = config.get(
            "properties", PneumaticOnOffActuator_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
