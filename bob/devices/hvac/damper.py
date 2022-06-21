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
    Electricity_24V_60HzInletConnectionPoint,
    Electricity_120V_60HzInletConnectionPoint,
)
from ...connections.light import (
    LightOutletConnectionPoint,
    LightVisibleOutletConnectionPoint,
)
from ...core import Device, PropertyReference, BOB, logging, P223, S223, template_update
from ...functions import AnalogInput, AnalogOutput
from ...properties import Nm, Percent, PercentCommand
from .actuator import (
    ElectricalOnOffActuator,
    ElectricalProportionalActuator,
    PneumaticOnOffActuator,
    PneumaticProportionalActuator,
)

_namespace = BOB


# DAMPERS


class Damper(Device):
    _class_iri = S223.Damper
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    command: PropertyReference
    feedback: PropertyReference
    # position: ActuatableProperty


class GravityDamper(Damper):
    _class_iri = S223.Damper


class FireDamper(Damper):
    _class_iri = S223.Damper


# DAMPER + ACTUATORS


electrical_actuated_proportional_damper_template = {
    "devices": {("actuator", ElectricalProportionalActuator): {}},
    "properties": {
        ("position", PercentCommand): {},
    },
}

electrical_actuated_onoff_damper_template = {
    "devices": {("actuator", ElectricalOnOffActuator): {}},
    "properties": {
        ("position", OnOffCommand): {},
    },
}


class ElectricalActuatedProportionalDamper(Damper):
    _class_iri: URIRef = S223.Damper

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            electrical_actuated_proportional_damper_template, config
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        logging.debug(
            f"ElectricalActuatedProportionalDamper.__init__ {_config} {kwargs}"
        )
        super().__init__(_config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedback = self["actuator"]["feedback"]
        self["actuator"].actuatesProperty = self["position"]
        # TODO : ExtRef of position


class ElectricalActuatedOnOffDamper(Damper):
    _class_iri: URIRef = S223.Damper

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(electrical_actuated_onoff_damper_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedbackOpen = self["actuator"]["feedbackOpen"]
        self.feedbackClose = self["actuator"]["feedbackClose"]
        self["actuator"].actuatesProperty = self["position"]
        # TODO : ExtRef of position


pneumatic_actuated_proportional_damper_template = {
    "devices": {("actuator", PneumaticProportionalActuator): {}},
    "properties": {
        ("position", PercentCommand): {},
    },
}
pneumatic_actuated_onoff_damper_template = {
    "devices": {("actuator", PneumaticOnOffActuator): {}},
    "properties": {
        ("position", OnOffCommand): {},
    },
}


class PneumaticActuatedProportionalDamper(Damper):
    _class_iri = S223.Damper

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            pneumatic_actuated_proportional_damper_template, config
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedback = self["actuator"]["feedback"]
        self["actuator"].actuatesProperty = self["position"]
        # TODO : ExtRef of position


class PneumaticActuatedOnOffDamper(Damper):
    _class_iri = S223.Damper

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(pneumatic_actuated_onoff_damper_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedbackOpen = self["actuator"]["feedbackOpen"]
        self.feedbackClose = self["actuator"]["feedbackClose"]
        self["actuator"].actuatesProperty = self["position"]
        # TODO : ExtRef of position
