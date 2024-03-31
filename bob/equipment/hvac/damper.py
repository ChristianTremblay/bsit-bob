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
from ...template import template_update
from .actuator import (
    BaseActuator,
    ElectricalOnOffActuator,
    ElectricalProportionalActuator,
    PneumaticOnOffActuator,
    PneumaticProportionalActuator,
)

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB


# DAMPERS


class Damper(Equipment):
    _class_iri = S223.Damper
    linkageInlet: MechanicalInletConnectionPoint
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    position: PropertyReference
    command: PropertyReference
    position_feedback: PropertyReference
    is_open: PropertyReference
    is_closed: PropertyReference


class GravityDamper(Damper):
    _class_iri = S223.Damper


class FireDamper(Damper):
    _class_iri = S223.Damper


# ======
# Systems definition
#
# Below are associations of damper + actuator with different configurations
# to be used in models
#
# ======

actuated_damper_template = {
    "equipment": {
        # ("actuator", BaseActuator): {},
        # ("damper", Damper): {},
    },
}


class DamperAndActuator(Equipment):
    _class_iri = None
    airInlet: AirInletConnectionPoint  # will be defined as equal to damper
    airOutlet: AirOutletConnectionPoint  # will be defined as equal to damper
    position: PropertyReference
    command: PropertyReference
    position_feedback: PropertyReference
    is_open: PropertyReference
    is_closed: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.command = self["damper"]["command"] = self["actuator"]["command"]
        self.is_open = self["damper"]["is_open"] = self["actuator"]["is_open"]
        self.is_closed = self["damper"]["is_closed"] = self["actuator"]["is_closed"]
        self["actuator"].linkageOutlet >> self["damper"].linkageInlet
        self.position = self["damper"].position = self["actuator"].position
        self.position_feedback = self["actuator"]["position_sensor"].observedProperty
        self["damper"].airInlet.maps_to(self.airInlet)
        self["damper"].airOutlet.maps_to(self.airOutlet)


electrical_actuated_proportional_damper_template = {
    "equipment": {
        ("actuator", ElectricalProportionalActuator): {},
        ("damper", Damper): {},
    },
    "properties": {},
}

electrical_actuated_onoff_damper_template = {
    "equipment": {("actuator", ElectricalOnOffActuator): {}, ("damper", Damper): {}},
    "properties": {},
}


class ElectricalActuatedProportionalDamper(DamperAndActuator):
    _class_iri: URIRef = BOB.ElectricalActuatedProportionalDamper

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            electrical_actuated_proportional_damper_template, config
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"ElectricalActuatedProportionalDamper.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)


class ElectricalActuatedOnOffDamper(DamperAndActuator):
    _class_iri: URIRef = BOB.ElectricalActuatedOnOffDamper

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(electrical_actuated_onoff_damper_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


pneumatic_actuated_proportional_damper_template = {
    "equipment": {
        ("actuator", PneumaticProportionalActuator): {},
        ("damper", Damper): {},
    },
    "properties": {},
}
pneumatic_actuated_onoff_damper_template = {
    "equipment": {("actuator", PneumaticOnOffActuator): {}, ("damper", Damper): {}},
    "properties": {},
}


class PneumaticActuatedProportionalDamper(DamperAndActuator):
    _class_iri = BOB.PneumaticActuatedProportionalDamper

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            pneumatic_actuated_proportional_damper_template, config
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


class PneumaticActuatedOnOffDamper(DamperAndActuator):
    _class_iri = BOB.PneumaticActuatedOnOffDamper

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(pneumatic_actuated_onoff_damper_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
