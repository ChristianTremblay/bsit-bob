from typing import Any, Dict

from rdflib import URIRef

from bob.connections.air import (
    CompressedAirInletConnectionPoint,
    CompressedAirOutletConnectionPoint,
)
from bob.connections.naturalgas import (
    NaturalGasInletConnectionPoint,
    NaturalGasOutletConnectionPoint,
)
from bob.properties.ratio import PercentCommand

from ...connections.electricity import (
    ModulationSignalInletConnectionPoint,
    OnOffSignalInletConnectionPoint,
)
from ...connections.water import (
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...core import Device, PropertyReference, s223
from ...properties import Gallons, Percent
from .actuator import ElectricalActuator

_namespace = s223

valve2w_template = {
    "cp": {
        "waterInlet": WaterInletConnectionPoint,
        "waterOutlet": WaterOutletConnectionPoint,
        "positionInlet": ModulationSignalInletConnectionPoint,
        "onOffInlet": OnOffSignalInletConnectionPoint,
    },
    "properties": {
        ("flowCoefficient", Gallons): {},
    },
}

valve_3w_diverting_template = {
    "cp": {
        "waterInletAB": WaterInletConnectionPoint,
        "waterOutletA": WaterOutletConnectionPoint,
        "waterOutletB": WaterOutletConnectionPoint,
        "positionInlet": ModulationSignalInletConnectionPoint,
        "onOffInlet": OnOffSignalInletConnectionPoint,
    },
    "properties": {
        ("flowCoefficient", Gallons): {},
    },
}

valve_3w_mixing_template = {
    "cp": {
        "waterInletAB": WaterInletConnectionPoint,
        "waterOutletA": WaterOutletConnectionPoint,
        "waterOutletB": WaterOutletConnectionPoint,
        "positionInlet": ModulationSignalInletConnectionPoint,
        "onOffInlet": OnOffSignalInletConnectionPoint,
    },
    "properties": {
        ("flowCoefficient", Gallons): {},
    },
}


class Valve(Device):
    _class_iri: URIRef = s223.Valve
    position: PropertyReference
    feedback: PropertyReference


class TwoWayValve(Valve):
    _class_iri: URIRef = s223.Valve

    def __init__(self, config: Dict = valve2w_template, **kwargs):
        config["properties"] = config.get("properties", valve2w_template["properties"])
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class ThreeWayValveDiverting(Valve):
    """
    A diverting valve has 1 inlet and 2 outlets
    """

    _class_iri: URIRef = s223.Valve

    def __init__(self, config: Dict = valve_3w_diverting_template, **kwargs):
        config["properties"] = config.get(
            "properties", valve_3w_diverting_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class ThreeWayValveMixing(Valve):
    """
    A mixing valve has 2 inlet and 1 outlet
    """

    _class_iri: URIRef = s223.Valve

    def __init__(self, config: Dict = valve_3w_mixing_template, **kwargs):
        config["properties"] = config.get(
            "properties", valve_3w_mixing_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class NaturalGasValve(TwoWayValve):
    _class_iri: URIRef = s223.NaturalGasValve
    naturalGasInlet: NaturalGasInletConnectionPoint
    naturalGasOutlet: NaturalGasOutletConnectionPoint


class PneumaticValve(TwoWayValve):
    _class_iri: URIRef = s223.PneumaticValve
    compressedAirInlet: CompressedAirInletConnectionPoint
    compressedAirOutlet: CompressedAirOutletConnectionPoint


actuated_valve_template = {
    "devices": {("actuator", ElectricalActuator): {}},
    "properties": {},
}


class TwoWayActuatedValve(TwoWayValve):
    node_type: URIRef = s223.Valve

    def __init__(
        self, config: Dict = {**actuated_valve_template, **valve2w_template}, **kwargs
    ):
        config["properties"] = config.get(
            "properties", {**actuated_valve_template, **valve2w_template}["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.position = self["actuator"]["position"]
        self.torque = self["actuator"]["torque"]
        self["actuator"].actuates = self


class ThreeWayMixingActuatedValve(ThreeWayValveMixing):
    node_type: URIRef = s223.Valve

    def __init__(
        self,
        config: Dict = {**actuated_valve_template, **valve_3w_mixing_template},
        **kwargs
    ):
        config["properties"] = config.get(
            "properties",
            {**actuated_valve_template, **valve_3w_mixing_template}["properties"],
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.position = self["actuator"]["position"]
        self.torque = self["actuator"]["torque"]
        self["actuator"].actuates = self


class ThreeWayDivertingActuatedValve(ThreeWayValveDiverting):
    node_type: URIRef = s223.Valve

    def __init__(
        self,
        config: Dict = {**actuated_valve_template, **valve_3w_diverting_template},
        **kwargs
    ):
        config["properties"] = config.get(
            "properties",
            {**actuated_valve_template, **valve_3w_diverting_template}["properties"],
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.position = self["actuator"]["position"]
        self.torque = self["actuator"]["torque"]
        self["actuator"].actuates = self
