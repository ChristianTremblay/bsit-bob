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
from ...core import (
    Device,
    logging,
    Node,
    PropertyReference,
    BOB,
    P223,
    S223,
    template_update,
)
from ...properties import Gallons, Percent
from .actuator import ElectricalOnOffActuator, ElectricalProportionalActuator

_namespace = BOB

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
    _class_iri: URIRef = S223.Valve
    command: PropertyReference
    position: ActuatableProperty

    def __init__(self, config: Dict = {}, **kwargs):
        logging.debug(f"Valve.__init__ {config} {kwargs}")
        super().__init__(config, **kwargs)
        # TODO find a way to do that
        # self.position = self.feedback if self.feedback else self.command


class TwoWayValve(Valve):
    _class_iri: URIRef = S223.Valve

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(valve2w_template, config)
        kwargs = {**_config.get("params", {}), **kwargs}
        logging.debug(f"TwoWayValve.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)


class ThreeWayValveDiverting(Valve):
    """
    A diverting valve has 1 inlet and 2 outlets
    """

    _class_iri = S223.Valve

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(valve_3w_diverting_template, config)
        kwargs = {**_config.get("params", {}), **kwargs}
        logging.debug(f"ThreeWayValveDiverting.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)


class ThreeWayValveMixing(Valve):
    """
    A mixing valve has 2 inlet and 1 outlet
    """

    _class_iri: URIRef = S223.Valve

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(valve_3w_mixing_template, config)
        kwargs = {**_config.get("params", {}), **kwargs}
        logging.debug(f"ThreeWayValveMixing.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)


class NaturalGasValve(TwoWayValve):
    _class_iri = S223.Valve
    naturalGasInlet: NaturalGasInletConnectionPoint
    naturalGasOutlet: NaturalGasOutletConnectionPoint


class PneumaticValve(TwoWayValve):
    _class_iri = S223.Valve
    compressedAirInlet: CompressedAirInletConnectionPoint
    compressedAirOutlet: CompressedAirOutletConnectionPoint


electrical_actuated_proportional_valve_template = {
    "devices": {("actuator", ElectricalProportionalActuator): {}},
    "properties": {
        ("position", PercentCommand): {},
    },
}

electrical_actuated_onoff_valve_template = {
    "devices": {("actuator", ElectricalOnOffActuator): {}},
    "properties": {
        ("position", OpenCloseCommand): {},
    },
}


class TwoWayActuatedProportionalValve(TwoWayValve):
    _class_iri = S223.Valve
    feedback: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            bases=[valve2w_template, electrical_actuated_proportional_valve_template],
            config=config,
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        logging.debug(f"TwoWayActuatedProportionalValve.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedback = self["actuator"]["feedback"]
        self.torque = self["actuator"]["torque"]
        #self["actuator"]["command"].actuatesProperty = self["position"] # people arent' ready for that .... yet
        self["actuator"].actuatesProperty = self["position"]
        # TODO : ExtRef of position


class TwoWayActuatedOnOffValve(TwoWayValve):
    _class_iri = S223.Valve
    feedbackOpen: PropertyReference
    feedbackClose: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            bases=[valve2w_template, electrical_actuated_onoff_valve_template],
            config=config,
        )
        kwargs = {**_config.get("params", {}), **kwargs}
        logging.debug(f"TwoWayActuatedOnOffValve.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)
        self.feedbackOpen = self["actuator"]["feedbackOpen"]
        self.feedbackClose = self["actuator"]["feedbackClose"]
        self.command = self["actuator"]["command"]
        #self["actuator"]["command"].actuatesProperty = self["position"] # people arent' ready for that .... yet
        self["actuator"].actuatesProperty = self["position"]
        # TODO : ExtRef of position


class ThreeWayMixingActuatedProportionalValve(ThreeWayValveMixing):
    node_type = S223.Valve
    feedback: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            bases=[
                valve_3w_mixing_template,
                electrical_actuated_proportional_valve_template,
            ],
            config=config,
        )
        kwargs = {**_config.get("params", {}), **kwargs}
        logging.debug(
            f"ThreeWayMixingActuatedProportionalValve.__init__ {_config} {kwargs}"
        )
        super().__init__(_config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedback = self["actuator"]["feedback"]
        #self["actuator"]["command"].actuatesProperty = self["position"] # people arent' ready for that .... yet
        self["actuator"].actuatesProperty = self["position"]
        # TODO : ExtRef of position


class ThreeWayMixingActuatedOnOffValve(ThreeWayValveMixing):
    _class_iri = S223.Valve
    feedbackOpen: PropertyReference
    feedbackClose: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            bases=[valve_3w_mixing_template, electrical_actuated_onoff_valve_template],
            config=config,
        )
        kwargs = {**_config.get("params", {}), **kwargs}
        logging.debug(f"ThreeWayMixingActuatedOnOffValve.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)
        self.feedbackOpen = self["actuator"]["feedbackOpen"]
        self.feedbackClose = self["actuator"]["feedbackClose"]
        #self["actuator"]["command"].actuatesProperty = self["position"] # people arent' ready for that .... yet
        self["actuator"].actuatesProperty = self["position"]
        # TODO : ExtRef of position


class ThreeWayDivertingActuatedProportionalValve(ThreeWayValveDiverting):
    _class_iri = S223.Valve
    feedback: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            bases=[
                valve_3w_diverting_template,
                electrical_actuated_proportional_valve_template,
            ],
            config=config,
        )
        kwargs = {**_config.get("params", {}), **kwargs}
        logging.debug(
            f"ThreeWayDivertingActuatedProportionalValve.__init__ {_config} {kwargs}"
        )
        super().__init__(_config, **kwargs)
        self.command = self["actuator"]["command"]
        self.feedback = self["actuator"]["feedback"]
        #self["actuator"]["command"].actuatesProperty = self["position"] # people arent' ready for that .... yet
        self["actuator"].actuatesProperty = self["position"]
        # TODO : ExtRef of position


class ThreeWayDivertingActuatedOnOffValve(ThreeWayValveDiverting):
    _class_iri = S223.Valve
    feedbackOpen: PropertyReference
    feedbackClose: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            bases=[
                valve_3w_diverting_template,
                electrical_actuated_onoff_valve_template,
            ],
            config=config,
        )
        kwargs = {**_config.get("params", {}), **kwargs}
        logging.debug(
            f"ThreeWayDivertingActuatedOnOffValve.__init__ {_config} {kwargs}"
        )
        super().__init__(_config, **kwargs)
        self.feedbackOpen = self["actuator"]["feedbackOpen"]
        self.feedbackClose = self["actuator"]["feedbackClose"]
        self.command = self["actuator"]["command"]
        #self["actuator"]["command"].actuatesProperty = self["position"] # people arent' ready for that .... yet
        self["actuator"].actuatesProperty = self["position"]
        # TODO : ExtRef of position
