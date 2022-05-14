from typing import Dict

from rdflib import URIRef

from bob.properties import Nm, Percent, PercentCommand

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

_namespace = s223

# ACTUATORS


class DamperActuator(Device):
    node_type = s223.DamperActuator
    position: PercentCommand
    feedback: Percent
    torque: Nm


ElectricalActuator_template = {
    "cp": {"electricalInlet": Electricity_24V_60HzInletConnectionPoint},
    "properties": {
        ("position", PercentCommand): {},
        ("feedback", Percent): {},
        ("torque", Nm): {},
    },
}


class ElectricalActuator(DamperActuator):
    node_type = s223.DamperActuator

    def __init__(self, config: Dict = ElectricalActuator_template, **kwargs):
        config["properties"] = config.get(
            "properties", ElectricalActuator_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


PneumaticActuator_template = {
    "cp": {},
    "properties": {
        ("position", PercentCommand): {},
        ("feedback", Percent): {},
        ("torque", Nm): {},
    },
}


class PneumaticActuator(DamperActuator):
    node_type = s223.DamperActuator
    compressedAirInlet: CompressedAirInletConnectionPoint

    def __init__(self, config: Dict = PneumaticActuator_template, **kwargs):
        config["properties"] = config.get(
            "properties", PneumaticActuator_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
