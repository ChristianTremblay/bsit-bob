from typing import Any, Dict, Union

from rdflib import URIRef

from bob.connections.air import (
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
    CompressedAirInletConnectionPoint,
    CompressedAirOutletConnectionPoint,
)
from bob.connections.mechanical import MechanicalInletConnectionPoint
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
    WaterInletSystemConnectionPoint,
    WaterOutletConnectionPoint,
    WaterOutletSystemConnectionPoint,
)
from ...core import (
    BOB,
    P223,
    S223,
    Equipment,
    Node,
    PropertyReference,
    System,
    logging,
    template_update,
)
from ...properties import Gallons, Percent
from .actuator import ElectricalOnOffActuator, ElectricalProportionalActuator

_namespace = BOB


class Valve(Equipment):
    """
    Base class for a valve. Must be subclassed to provide inlet and outlet
    depending on configuration
    """

    _class_iri: URIRef = S223.Valve
    linkageInlet: MechanicalInletConnectionPoint
    position: Percent
    command: PropertyReference
    position_feedback: PropertyReference
    is_open: PropertyReference
    is_closed: PropertyReference
    flowCoefficient: Gallons


class TwoWayValve(Valve):
    """
    Two-way valve have 1 inlet and 1 outlet
    """

    _class_iri: URIRef = S223.Valve
    waterInlet: WaterInletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint


class ThreeWayValveDiverting(Valve):
    """
    A diverting valve has 1 inlet and 2 outlets
    """

    _class_iri = S223.Valve
    waterInletAB: WaterInletConnectionPoint
    waterOutletA: WaterOutletConnectionPoint
    waterOutletB: WaterOutletConnectionPoint


class ThreeWayValveMixing(Valve):
    """
    A mixing valve has 2 inlet and 1 outlet
    """

    _class_iri: URIRef = S223.Valve
    waterInletA: WaterInletConnectionPoint
    waterInletB: WaterOutletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint


class NaturalGasValve(Valve):
    _class_iri = S223.Valve
    naturalGasInlet: NaturalGasInletConnectionPoint
    naturalGasOutlet: NaturalGasOutletConnectionPoint


class PneumaticValve(Valve):
    _class_iri = S223.Valve
    compressedAirInlet: CompressedAirInletConnectionPoint
    compressedAirOutlet: CompressedAirOutletConnectionPoint


# ======
# Systems definition
#
# Below are associations of valve + actuators with different configuration
# to be used in models
#
# ======


class TwoWayActuatedValve(System):
    """
    This base class allow the creation of SystemConnectionPoints
    via the config mechanism
    """

    _class_iri = None
    waterInlet: WaterInletSystemConnectionPoint
    waterOutlet: WaterOutletSystemConnectionPoint
    position: PropertyReference
    command: PropertyReference
    position_feedback: PropertyReference
    is_open: PropertyReference
    is_closed: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)

        self.command = self["valve"]["command"] = self["actuator"]["command"]
        self["is_open"] = self["valve"]["is_open"] = self["actuator"]["is_open"]
        self["is_closed"] = self["valve"]["is_closed"] = self["actuator"]["is_closed"]
        self["actuator"].linkageOutlet >> self["valve"].linkageInlet
        self["position"] = self["valve"]["position"] = self["actuator"]["position"]
        self["position_feedback"] = self["actuator"]["position_sensor"].observesProperty
        self.waterInlet.mapsTo = self["valve"].waterInlet
        self.waterOutlet.mapsTo = self["valve"].waterOutlet


electrical_actuated_proportional_2w_valve_template = {
    "equipment": {
        ("actuator", ElectricalProportionalActuator): {},
        ("valve", TwoWayValve): {},
    },
    "properties": {},
}


class TwoWayActuatedProportionalValve(TwoWayActuatedValve):
    _class_iri = BOB.TwoWayActuatedProportionalValve

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            electrical_actuated_proportional_2w_valve_template, config
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        logging.debug(f"TwoWayActuatedProportionalValve.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)


electrical_actuated_onoff_2w_valve_template = {
    "equipment": {
        ("actuator", ElectricalOnOffActuator): {},
        ("valve", TwoWayValve): {},
    },
    "properties": {},
}


class TwoWayActuatedOnOffValve(TwoWayActuatedValve):
    _class_iri = BOB.TwoWayActuatedOnOffValve

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(electrical_actuated_onoff_2w_valve_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


class ThreeWayActuatedValve(System):
    """
    This base class allow the creation of SystemConnectionPoints
    via the config mechanism
    """

    _class_iri = None

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.command = self["valve"]["command"] = self["actuator"]["command"]
        self["is_open"] = self["valve"]["is_open"] = self["actuator"]["is_open"]
        self["is_closed"] = self["valve"]["is_closed"] = self["actuator"]["is_closed"]
        self["actuator"].linkageOutlet >> self["valve"].linkageInlet
        self["position"] = self["valve"]["position"] = self["actuator"]["position"]
        self["position_feedback"] = self["actuator"]["position_sensor"].observesProperty


class ThreeWayMixingSystem(ThreeWayActuatedValve):
    _class_iri = None
    waterInletAB: WaterInletSystemConnectionPoint
    waterOutletA: WaterOutletSystemConnectionPoint
    waterOutletB: WaterOutletSystemConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            {"equipment": {("valve", ThreeWayValveMixing): {}}}, config
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.waterInletAB.mapsTo = self["valve"].waterInletAB
        self.waterOutletA.mapsTo = self["valve"].waterOutletA
        self.waterOutletB.mapsTo = self["valve"].waterOutletB


class ThreeWayDivertingSystem(ThreeWayActuatedValve):
    _class_iri = None
    waterInletA: WaterInletSystemConnectionPoint
    waterInletB: WaterInletSystemConnectionPoint
    waterOutlet: WaterOutletSystemConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            {"equipment": {("valve", ThreeWayValveDiverting): {}}}, config
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.waterInletA.mapsTo = self["valve"].waterInletA
        self.waterInletB.mapsTo = self["valve"].waterInletB
        self.waterOutlet.mapsTo = self["valve"].waterOutlet


class ThreeWayMixingActuatedProportionalValve(ThreeWayMixingSystem):
    node_type = BOB.ThreeWayMixingActuatedProportionalValve

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            {"equipment": {("actuator", ElectricalProportionalActuator): {}}}, config
        )
        kwargs = {**_config.get("params", {}), **kwargs}
        logging.debug(
            f"ThreeWayMixingActuatedProportionalValve.__init__ {_config} {kwargs}"
        )
        super().__init__(_config, **kwargs)


class ThreeWayMixingActuatedOnOffValve(ThreeWayValveMixing):
    _class_iri = BOB.ThreeWayMixingActuatedOnOffValve

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            {"equipment": {("actuator", ElectricalOnOffActuator): {}}}, config
        )
        kwargs = {**_config.get("params", {}), **kwargs}
        logging.debug(f"ThreeWayMixingActuatedOnOffValve.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)


class ThreeWayDivertingActuatedProportionalValve(ThreeWayDivertingSystem):
    _class_iri = BOB.ThreeWayDivertingActuatedProportionalValve

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            {"equipment": {("actuator", ElectricalProportionalActuator): {}}}, config
        )
        kwargs = {**_config.get("params", {}), **kwargs}
        logging.debug(
            f"ThreeWayDivertingActuatedProportionalValve.__init__ {_config} {kwargs}"
        )
        super().__init__(_config, **kwargs)


class ThreeWayDivertingActuatedOnOffValve(ThreeWayValveDiverting):
    _class_iri = BOB.ThreeWayDivertingActuatedProportionalValve

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            {"equipment": {("actuator", ElectricalOnOffActuator): {}}}, config
        )
        kwargs = {**_config.get("params", {}), **kwargs}
        logging.debug(
            f"ThreeWayDivertingActuatedOnOffValve.__init__ {_config} {kwargs}"
        )
        super().__init__(_config, **kwargs)
