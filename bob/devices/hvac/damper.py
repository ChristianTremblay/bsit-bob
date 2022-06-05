from typing import Dict, Union

from rdflib import URIRef

from bob.properties.states import OnOffStatus, OpenCloseStatus

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
from ...core import Device, Node, PropertyReference, p223, s223
from ...properties import Nm, Percent, PercentCommand
from .actuator import (
    ElectricalOnOffActuator,
    ElectricalProportionalActuator,
    PneumaticOnOffActuator,
    PneumaticProportionalActuator,
)

_namespace = s223

# DAMPERS


class Damper(Device):
    _class_iri =s223.Damper
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    position: PropertyReference  # Union[Percent,OnOffStatus,OpenCloseStatus]
    command: PropertyReference
    feedback: PropertyReference


class GravityDamper(Damper):
    _class_iri =s223.Damper


class FireDamper(Damper):
    _class_iri =s223.Damper


# DAMPER + ACTUATORS


ElectricalActuatedProportionalDamper_template = {
    "devices": {("actuator", ElectricalProportionalActuator): {}},
    "properties": {},
}

ElectricalActuatedOnOffDamper_template = {
    "devices": {("actuator", ElectricalOnOffActuator): {}},
    "properties": {},
}


class ElectricalActuatedProportionalDamper(Damper):
    _class_iri: URIRef = s223.Damper

    def __init__(
        self, config: Dict = ElectricalActuatedProportionalDamper_template, **kwargs
    ):
        config["properties"] = config.get(
            "properties", ElectricalActuatedProportionalDamper_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedback = self["actuator"]["feedback"]
        self.position = self.feedback if self.feedback else self.command
        self["actuator"].actuatesProperty = self.position


class ElectricalActuatedOnOffDamper(Damper):
    _class_iri: URIRef = s223.Damper

    def __init__(self, config: Dict = ElectricalActuatedOnOffDamper_template, **kwargs):
        config["properties"] = config.get(
            "properties", ElectricalActuatedOnOffDamper_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedbackOpen = self["actuator"]["feedbackOpen"]
        self.feedbackClose = self["actuator"]["feedbackClose"]
        self.position = (
            self.command
        )  # feedbackOpen and close can't be used here... at least not for now or we'll end up with 3 states, [open, close, moving]
        self["actuator"].actuatesProperty = self.position


PneumaticActuatedProportionalDamper_template = {
    "devices": {("actuator", PneumaticProportionalActuator): {}},
    "properties": {},
}
PneumaticActuatedOnOffDamper_template = {
    "devices": {("actuator", PneumaticOnOffActuator): {}},
    "properties": {},
}


class PneumaticActuatedProportionalDamper(Damper):
    _class_iri =s223.Damper

    def __init__(
        self, config: Dict = PneumaticActuatedProportionalDamper_template, **kwargs
    ):
        config["properties"] = config.get(
            "properties", PneumaticActuatedProportionalDamper_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedback = self["actuator"]["feedback"]
        self.position = self.feedback if self.feedback else self.command
        self["actuator"].actuatesProperty = self.position


class PneumaticActuatedOnOffDamper(Damper):
    _class_iri =s223.Damper

    def __init__(self, config: Dict = PneumaticActuatedOnOffDamper_template, **kwargs):
        config["properties"] = config.get(
            "properties", PneumaticActuatedOnOffDamper_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedbackOpen = self["actuator"]["feedbackOpen"]
        self.feedbackClose = self["actuator"]["feedbackClose"]
        self.position = (
            self.command
        )  # feedbackOpen and close can't be used here... at least not for now or we'll end up with 3 states, [open, close, moving]
        self["actuator"].actuatesProperty = self.position
