from typing import Any, Dict, Union

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
from bob.properties.states import OnOffCommand, OnOffStatus, OpenCloseStatus

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
from ...core import Device, Node, PropertyReference, s223
from ...properties import Gallons, Percent
from .actuator import ElectricalOnOffActuator, ElectricalProportionalActuator

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
    position: PropertyReference  # Union[Percent,OnOffStatus,OpenCloseStatus]
    command: PropertyReference
    feedback: PropertyReference

    def __init__(self, config: Dict = {}, **kwargs):
        super().__init__(config, **kwargs)
        # TODO find a way to do that
        # self.position = self.feedback if self.feedback else self.command


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
    _class_iri: URIRef = s223.Valve
    naturalGasInlet: NaturalGasInletConnectionPoint
    naturalGasOutlet: NaturalGasOutletConnectionPoint


class PneumaticValve(TwoWayValve):
    _class_iri: URIRef = s223.Valve
    compressedAirInlet: CompressedAirInletConnectionPoint
    compressedAirOutlet: CompressedAirOutletConnectionPoint


ActuatedProportionalValve_template = {
    "devices": {("actuator", ElectricalProportionalActuator): {}},
    "properties": {},
}

ActuatedOnOffValve_template = {
    "devices": {("actuator", ElectricalOnOffActuator): {}},
    "properties": {},
}


class TwoWayActuatedProportionalValve(TwoWayValve):
    _class_iri: URIRef = s223.Valve

    def __init__(
        self,
        config: Dict = {**ActuatedProportionalValve_template, **valve2w_template},
        **kwargs
    ):
        config["properties"] = config.get(
            "properties",
            {**ActuatedProportionalValve_template, **valve2w_template}["properties"],
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedback = self["actuator"]["feedback"]
        self.position = self.feedback if self.feedback else self.command
        self["actuator"].actuatesProperty = self.position


class TwoWayActuatedOnOffValve(TwoWayValve):
    _class_iri: URIRef = s223.Valve

    def __init__(
        self,
        config: Dict = {**ActuatedOnOffValve_template, **valve2w_template},
        **kwargs
    ):
        config["properties"] = config.get(
            "properties",
            {**ActuatedOnOffValve_template, **valve2w_template}["properties"],
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.feedbackOpen = self["actuator"]["feedbackOpen"]
        self.feedbackClose = self["actuator"]["feedbackClose"]
        self.position = (
            self.command
        )  # feedbackOpen and close can't be used here... at least not for now or we'll end up with 3 states, [open, close, moving]
        self["actuator"].actuatesProperty = self.position


class ThreeWayMixingActuatedProportionalValve(ThreeWayValveMixing):
    _class_iri: URIRef = s223.Valve

    def __init__(
        self,
        config: Dict = {
            **ActuatedProportionalValve_template,
            **valve_3w_mixing_template,
        },
        **kwargs
    ):
        config["properties"] = config.get(
            "properties",
            {**ActuatedProportionalValve_template, **valve_3w_mixing_template}[
                "properties"
            ],
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedback = self["actuator"]["feedback"]
        self.position = self.feedback if self.feedback else self.command
        self["actuator"].actuatesProperty = self.position


class ThreeWayMixingActuatedOnOffValve(ThreeWayValveMixing):
    _class_iri: URIRef = s223.Valve

    def __init__(
        self,
        config: Dict = {**ActuatedOnOffValve_template, **valve_3w_mixing_template},
        **kwargs
    ):
        config["properties"] = config.get(
            "properties",
            {**ActuatedOnOffValve_template, **valve_3w_mixing_template}["properties"],
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.feedbackOpen = self["actuator"]["feedbackOpen"]
        self.feedbackClose = self["actuator"]["feedbackClose"]
        self.position = (
            self.command
        )  # feedbackOpen and close can't be used here... at least not for now or we'll end up with 3 states, [open, close, moving]
        self["actuator"].actuatesProperty = self.position


class ThreeWayDivertingActuatedProportionalValve(ThreeWayValveDiverting):
    _class_iri: URIRef = s223.Valve

    def __init__(
        self,
        config: Dict = {
            **ActuatedProportionalValve_template,
            **valve_3w_diverting_template,
        },
        **kwargs
    ):
        config["properties"] = config.get(
            "properties",
            {**ActuatedProportionalValve_template, **valve_3w_diverting_template}[
                "properties"
            ],
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedback = self["actuator"]["feedback"]
        self.position = self.feedback if self.feedback else self.command
        self["actuator"].actuatesProperty = self.position


class ThreeWayDivertingActuatedOnOffValve(ThreeWayValveDiverting):
    _class_iri: URIRef = s223.Valve

    def __init__(
        self,
        config: Dict = {**ActuatedOnOffValve_template, **valve_3w_diverting_template},
        **kwargs
    ):
        config["properties"] = config.get(
            "properties",
            {**ActuatedOnOffValve_template, **valve_3w_diverting_template}[
                "properties"
            ],
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.feedbackOpen = self["actuator"]["feedbackOpen"]
        self.feedbackClose = self["actuator"]["feedbackClose"]
        self.position = (
            self.command
        )  # feedbackOpen and close can't be used here... at least not for now or we'll end up with 3 states, [open, close, moving]
        self["actuator"].actuatesProperty = self.position
