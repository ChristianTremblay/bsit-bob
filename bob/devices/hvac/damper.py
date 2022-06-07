from typing import Dict

from rdflib import URIRef

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
from .actuator import ElectricalActuator, PneumaticActuator

_namespace = s223

class DamperActuator(Device):
    _class_iri = s223.DamperActuator
    position = AnalogOutput
    feedback = AnalogInput


class ElectricalDamperActuator(Device):
    _class_iri = s223.DamperActuator
    electricalInlet: ElectricalInletConnectionPoint
    position = AnalogOutput
    feedback = AnalogInput


class PneumaticDamperActuator(Device):
    _class_iri = s223.DamperActuator
    compressedAirInlet: CompressedAirInletConnectionPoint
    position = AnalogOutput
    feedback = AnalogInput

# DAMPERS

class Damper(Device):
    _class_iri = s223.Damper
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    position: PropertyReference
    feedback: PropertyReference


class GravityDamper(Damper):
    _class_iri = s223.Damper


class FireDamper(Damper):
    _class_iri = s223.Damper


class ActuatedDamper(Damper):
    _class_iri = s223.Damper


class ElectricalActuatedDamper(Damper):
    _class_iri = s223.Damper
    powerInlet: ElectricalInletConnectionPoint

# DAMPER + ACTUATORS

electrical_actuated_damper_template = {
    "devices": {("actuator", ElectricalActuator): {}},
    "properties": {},
}


class ElectricalActuatedDamper(Damper):
    _class_iri: URIRef = s223.Damper

    def __init__(self, config: Dict = electrical_actuated_damper_template, **kwargs):
        config["properties"] = config.get(
            "properties", electrical_actuated_damper_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.position = self["actuator"]["position"]
        self.torque = self["actuator"]["torque"]
        self["actuator"].actuates = self


class PneumaticDamper(Damper):
    _class_iri = s223.Damper
    compressedAirInlet: CompressedAirConnectionPoint


pneumatic_actuated_damper_template = {
    "devices": {("actuator", PneumaticActuator): {}},
    "properties": {},
}


class PneumaticActuatedDamper(Damper):
    _class_iri = s223.Damper

    def __init__(self, config: Dict = pneumatic_actuated_damper_template, **kwargs):
        config["properties"] = config.get(
            "properties", pneumatic_actuated_damper_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.position = self["actuator"]["position"]
        self.torque = self["actuator"]["torque"]
        self["actuator"].actuates = self


class Window(Device):
    _class_iri = p223.Window
    indoor: AirBidirectionalConnectionPoint
    outdoor: AirBidirectionalConnectionPoint
    naturalLight: LightVisibleOutletConnectionPoint
