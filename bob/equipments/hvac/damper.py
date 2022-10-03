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
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
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
from ...connections.mechanical import MechanicalInletConnectionPoint
from ...core import (
    BOB,
    P223,
    S223,
    Device,
    MechanicalCoupling,
    PropertyReference,
    System,
    logging,
    template_update,
)
from ...functions import AnalogInput, AnalogOutput
from ...properties import Nm, Percent, PercentCommand
from .actuator import (
    BaseActuator,
    ElectricalOnOffActuator,
    ElectricalProportionalActuator,
    PneumaticOnOffActuator,
    PneumaticProportionalActuator,
)

_namespace = BOB


# DAMPERS


class Damper(Device):
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
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    position: PropertyReference
    command: PropertyReference
    position_feedback: PropertyReference
    is_open: PropertyReference
    is_closed: PropertyReference


# DAMPER + ACTUATORS
actuated_damper_template = {
    "devices": {
        # ("actuator", BaseActuator): {},
        ("damper", Damper): {},
    },
}


class DamperAndActuator(System):
    _class_iri = BOB.DamperAndActuator
    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    position: PropertyReference
    command: PropertyReference
    position_feedback: PropertyReference
    is_open: PropertyReference
    is_closed: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(actuated_damper_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.airInlet.mapsTo = self["damper"].airInlet
        self.airOutlet.mapsTo = self["damper"].airOutlet
        self.command = self["damper"]["command"] = self["actuator"]["command"]
        self["is_open"] = self["damper"]["is_open"] = self["actuator"]["is_open"]
        self["is_closed"] = self["damper"]["is_closed"] = self["actuator"]["is_closed"]
        self["actuator"].linkageOutlet >> self["damper"].linkageInlet
        self["position"] = self["damper"]["position"] = self["actuator"]["position"]


electrical_actuated_proportional_damper_template = {
    "devices": {
        ("actuator", ElectricalProportionalActuator): {},
        ("damper", Damper): {},
    },
    "properties": {},
}

electrical_actuated_onoff_damper_template = {
    "devices": {("actuator", ElectricalOnOffActuator): {}, ("damper", Damper): {}},
    "properties": {},
}


class ElectricalActuatedProportionalDamper(DamperAndActuator):
    _class_iri: URIRef = BOB.ElectricalActuatedProportionalDamper

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            electrical_actuated_proportional_damper_template, config
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        logging.debug(
            f"ElectricalActuatedProportionalDamper.__init__ {_config} {kwargs}"
        )
        super().__init__(_config, **kwargs)


class ElectricalActuatedOnOffDamper(DamperAndActuator):
    _class_iri: URIRef = BOB.ElectricalActuatedOnOffDamper

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(electrical_actuated_onoff_damper_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


pneumatic_actuated_proportional_damper_template = {
    "devices": {
        ("actuator", PneumaticProportionalActuator): {},
        ("damper", Damper): {},
    },
    "properties": {},
}
pneumatic_actuated_onoff_damper_template = {
    "devices": {("actuator", PneumaticOnOffActuator): {}, ("damper", Damper): {}},
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
