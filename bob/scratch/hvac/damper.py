from typing import Dict

from rdflib import URIRef

from bob.connections.mechanical import MechanicalInletConnectionPoint
from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.core import SCRATCH, UNIT, logging, Equipment
from bob.equipment.hvac.damper import Damper as BaseDamper
from bob.properties.ratio import Percent
from bob.template import configure_relations, template_update

from .actuator import (
    ElectricalOnOffActuator,
    ElectricalProportionalActuator,
    PneumaticOnOffActuator,
    PneumaticProportionalActuator,
)

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = SCRATCH


# DAMPERS


class Damper(Equipment):
    # _class_iri = S223.Damper
    linkageInlet: MechanicalInletConnectionPoint
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    # position: PropertyReference
    # command: PropertyReference
    # position_feedback: PropertyReference
    # is_open: PropertyReference
    # is_closed: PropertyReference


class GravityDamper(BaseDamper):
    _class_iri = SCRATCH.GravityDamper


class FireDamper(BaseDamper):
    _class_iri = SCRATCH.FireDamper


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


class DamperAndActuator(Damper):
    """
    This is made as a equipment and not a system because it is a common group of equipment
    You will see the use of mapsTo in the damper and actuator to link the connection points

    """

    _class_iri = SCRATCH.DamperAndActuator
    # airInlet: AirInletConnectionPoint  # will be defined as equal to damper
    # airOutlet: AirOutletConnectionPoint  # will be defined as equal to damper
    # position: PropertyReference
    # command: PropertyReference
    # position_feedback: PropertyReference
    # is_open: PropertyReference
    # is_closed: PropertyReference

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
        ("damper", Damper): {
            "config": {
                "properties": {
                    ("position", Percent): {
                        "hasUnit": UNIT.PERCENT,
                        "comment": "Damper Effective Position",
                    },
                }
            },
        },
    },
    "properties": {
        ("position", Percent): {
            "hasUnit": UNIT.PERCENT,
            "comment": "Damper Effective Position",
        },
        ("command", Percent): {
            "hasUnit": UNIT.PERCENT,
            "comment": "Damper Position command",
        },
        ("position_feedback", Percent): {
            "hasUnit": UNIT.PERCENT,
            "comment": "Damper Position feedback",
        },
        # "is_open": PropertyReference,
        # "is_closed": PropertyReference,
    },
    "relations": [
        ("self['position']", "@", "self['damper']['position']"),
        (
            "self['position_feedback']",
            "@",
            'self["actuator"]["position_sensor"].observedProperty',
        ),
        ("self['command']", "@", "self['actuator']['command']"),
    ],
}

electrical_actuated_onoff_damper_template = {
    "equipment": {("actuator", ElectricalOnOffActuator): {}, ("damper", Damper): {}},
    "properties": {},
}


class ElectricalActuatedProportionalDamper(DamperAndActuator):
    _class_iri: URIRef = SCRATCH.ElectricalActuatedProportionalDamper

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            electrical_actuated_proportional_damper_template, config
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"ElectricalActuatedProportionalDamper.__init__ {_config} {kwargs}")
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)


class ElectricalActuatedOnOffDamper(DamperAndActuator):
    _class_iri: URIRef = SCRATCH.ElectricalActuatedOnOffDamper

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
    _class_iri = SCRATCH.PneumaticActuatedProportionalDamper

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            pneumatic_actuated_proportional_damper_template, config
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


class PneumaticActuatedOnOffDamper(DamperAndActuator):
    _class_iri = SCRATCH.PneumaticActuatedOnOffDamper

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(pneumatic_actuated_onoff_damper_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
