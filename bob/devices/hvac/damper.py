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
from ...core import Device, PropertyReference, p223, s223
from ...functions import AnalogInput, AnalogOutput
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
    _class_iri = s223.Damper
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    command: PropertyReference
    feedback: PropertyReference
    position: PropertyReference


class GravityDamper(Damper):
    _class_iri = s223.Damper


class FireDamper(Damper):
    _class_iri = s223.Damper


# DAMPER + ACTUATORS


electrical_actuated_proportional_damper_template = {
    "devices": {("actuator", ElectricalProportionalActuator): {}},
    "properties": {},
}

electrical_actuated_onoff_damper_template = {
    "devices": {("actuator", ElectricalOnOffActuator): {}},
    "properties": {},
}


class ElectricalActuatedProportionalDamper(Damper):
    _class_iri: URIRef = s223.Damper

    def __init__(
        self, config: Dict = electrical_actuated_proportional_damper_template, **kwargs
    ):
        config["properties"] = config.get(
            "properties", electrical_actuated_proportional_damper_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedback = self["actuator"]["feedback"]
        self.position = (
            self["actuator"]["feedback"]
            if self["actuator"]["feedback"]
            else self["actuator"]["command"]
        )
        self["actuator"].actuatesProperty = self.position


class ElectricalActuatedOnOffDamper(Damper):
    _class_iri: URIRef = s223.Damper

    def __init__(
        self, config: Dict = electrical_actuated_onoff_damper_template, **kwargs
    ):
        config["properties"] = config.get(
            "properties", electrical_actuated_onoff_damper_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedbackOpen = self["actuator"]["feedbackOpen"]
        self.feedbackClose = self["actuator"]["feedbackClose"]
        self.position = self["actuator"][
            "command"
        ]  # TODO Discussion required here... the concept of position when feedbackOpen and feedbackClose is avialable... it's super close from telemetry... how could we communicate the concept that if feedback is avialable, you can infer the position from validating both feedback. Then you will know if the thing is open, close or moving. Else, command becomes the position.
        self["actuator"].actuatesProperty = self.position


pneumatic_actuated_proportional_damper_template = {
    "devices": {("actuator", PneumaticProportionalActuator): {}},
    "properties": {},
}
pneumatic_actuated_onoff_damper_template = {
    "devices": {("actuator", PneumaticOnOffActuator): {}},
    "properties": {},
}


class PneumaticActuatedProportionalDamper(Damper):
    _class_iri = s223.Damper

    def __init__(
        self, config: Dict = pneumatic_actuated_proportional_damper_template, **kwargs
    ):
        config["properties"] = config.get(
            "properties", pneumatic_actuated_proportional_damper_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedback = self["actuator"]["feedback"]
        self.position = (
            self["actuator"]["feedback"]
            if self["actuator"]["feedback"]
            else self["actuator"]["command"]
        )
        self["actuator"].actuatesProperty = self.position


class PneumaticActuatedOnOffDamper(Damper):
    _class_iri = s223.Damper

    def __init__(
        self, config: Dict = pneumatic_actuated_onoff_damper_template, **kwargs
    ):
        config["properties"] = config.get(
            "properties", pneumatic_actuated_onoff_damper_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedbackOpen = self["actuator"]["feedbackOpen"]
        self.feedbackClose = self["actuator"]["feedbackClose"]
        self.position = self["actuator"]["command"]
        self["actuator"].actuatesProperty = self.position
