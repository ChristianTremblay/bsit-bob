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
from ...properties import Nm, Percent, PercentCommand
from .actuator import ElectricalActuator, PneumaticActuator

_namespace = s223

# DAMPERS


class Damper(Device):
    node_type = s223.Damper
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    position: PropertyReference
    feedback: PropertyReference


class GravityDamper(Damper):
    node_type = s223.Damper


class FireDamper(Damper):
    node_type = s223.Damper


# DAMPER + ACTUATORS


ElectricalActuatedDamper_template = {
    "devices": {("actuator", ElectricalActuator): {}},
    "properties": {},
}


class ElectricalActuatedDamper(Damper):
    node_type: URIRef = s223.Damper

    def __init__(self, config: Dict = ElectricalActuatedDamper_template, **kwargs):
        config["properties"] = config.get(
            "properties", ElectricalActuatedDamper_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.position = self["actuator"]["position"]
        self.torque = self["actuator"]["torque"]
        self["actuator"].actuates = self


PneumaticActuatedDamper_template = {
    "devices": {("actuator", PneumaticActuator): {}},
    "properties": {},
}


class PneumaticActuatedDamper(Damper):
    node_type = s223.Damper

    def __init__(self, config: Dict = PneumaticActuatedDamper_template, **kwargs):
        config["properties"] = config.get(
            "properties", PneumaticActuatedDamper_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.position = self["actuator"]["position"]
        self.torque = self["actuator"]["torque"]
        self["actuator"].actuates = self
