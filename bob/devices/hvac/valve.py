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
from bob.properties.states import (
    OnOffCommand,
    OnOffStatus,
    OpenCloseCommand,
    OpenCloseStatus,
)
from bob.property import ActuatableProperty

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
    command: PropertyReference
    position: ActuatableProperty

    def __init__(self, config: Dict = {}, **kwargs):
        super().__init__(config, **kwargs)
        # TODO find a way to do that
        # self.position = self.feedback if self.feedback else self.command


class TwoWayValve(Valve):
    _class_iri: URIRef = s223.Valve

    def __init__(self, config: Dict = valve2w_template, **kwargs):
        _config = valve2w_template
        if config:
            _config.update(config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


class ThreeWayValveDiverting(Valve):
    """
    A diverting valve has 1 inlet and 2 outlets
    """

    _class_iri = s223.Valve

    def __init__(self, config: Dict = None, **kwargs):
        _config = valve_3w_diverting_template
        if config:
            _config.update(config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


class ThreeWayValveMixing(Valve):
    """
    A mixing valve has 2 inlet and 1 outlet
    """

    _class_iri: URIRef = s223.Valve

    def __init__(self, config: Dict = None, **kwargs):
        _config = valve_3w_mixing_template
        if config:
            _config.update(config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


class NaturalGasValve(TwoWayValve):
    _class_iri = s223.NaturalGasValve
    naturalGasInlet: NaturalGasInletConnectionPoint
    naturalGasOutlet: NaturalGasOutletConnectionPoint


class PneumaticValve(TwoWayValve):
    _class_iri = s223.PneumaticValve
    compressedAirInlet: CompressedAirInletConnectionPoint
    compressedAirOutlet: CompressedAirOutletConnectionPoint


electrical_actuated_proportional_valve_template = {
    "devices": {("actuator", ElectricalProportionalActuator): {}},
    "properties": {
        ("feedback", PropertyReference): {},
        ("position", PercentCommand): {},
    },
}

electrical_actuated_onoff_valve_template = {
    "devices": {("actuator", ElectricalOnOffActuator): {}},
    "properties": {
        ("feedbackOpen", PropertyReference): {},
        ("feedbackClose", PropertyReference): {},
        ("position", OpenCloseCommand): {},
    },
}


class TwoWayActuatedProportionalValve(TwoWayValve):
    _class_iri = s223.Valve

    def __init__(
        self,
        config: Dict = None,
        **kwargs
    ):
        _config = valve2w_template
        _config.update(electrical_actuated_proportional_valve_template)
        if config:
            _config.update(config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedback = self["actuator"]["feedback"]
        self.torque = self["actuator"]["torque"]
        #self["actuator"].actuatesProperty = self['position']
        # TODO : ExtRef of position


class TwoWayActuatedOnOffValve(TwoWayValve):
    _class_iri = s223.Valve

    def __init__(
        self,
        config: Dict = None,
        **kwargs
    ):
        _config = valve2w_template
        _config.update(electrical_actuated_onoff_valve_template)
        if config:
            _config.update(config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.feedbackOpen = self["actuator"]["feedbackOpen"]
        self.feedbackClose = self["actuator"]["feedbackClose"]
        self.command = self["actuator"]["command"]
        self["actuator"].actuatesProperty = self['position']
        # TODO : ExtRef of position


class ThreeWayMixingActuatedProportionalValve(ThreeWayValveMixing):
    node_type = s223.Valve

    def __init__(
        self,
        config: Dict = None,
        **kwargs
    ):
        _config = valve_3w_mixing_template
        _config.update(electrical_actuated_proportional_valve_template)
        if config:
            _config.update(config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedback = self["actuator"]["feedback"]
        self["actuator"].actuatesProperty = self['position']
        # TODO : ExtRef of position


class ThreeWayMixingActuatedOnOffValve(ThreeWayValveMixing):
    _class_iri = s223.Valve

    def __init__(
        self,
        config: Dict = None,
        **kwargs
    ):
        _config = valve_3w_mixing_template
        _config.update(electrical_actuated_onoff_valve_template)
        if config:
            _config.update(config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.feedbackOpen = self["actuator"]["feedbackOpen"]
        self.feedbackClose = self["actuator"]["feedbackClose"]
        self["actuator"].actuatesProperty = self['position']
        # TODO : ExtRef of position


class ThreeWayDivertingActuatedProportionalValve(ThreeWayValveDiverting):
    _class_iri = s223.Valve

    def __init__(
        self,
        config: Dict = None,
        **kwargs
    ):
        _config = valve_3w_diverting_template
        _config.update(electrical_actuated_proportional_valve_template)
        if config:
            _config.update(config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedback = self["actuator"]["feedback"]
        self["actuator"].actuatesProperty = self['position']
        # TODO : ExtRef of position


class ThreeWayDivertingActuatedOnOffValve(ThreeWayValveDiverting):
    _class_iri = s223.Valve

    def __init__(
        self,
        config: Dict = None,
        **kwargs
    ):

        _config = valve_3w_diverting_template
        _config.update(electrical_actuated_onoff_valve_template)
        if config:
            _config.update(config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.feedbackOpen = self["actuator"]["feedbackOpen"]
        self.feedbackClose = self["actuator"]["feedbackClose"]
        self.command = self["actuator"]["command"]
        self["actuator"].actuatesProperty = self['position']
        # TODO : ExtRef of position
