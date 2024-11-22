from typing import Dict


from bob.equipment.hvac.valve import (
    TwoWayValve,
    ThreeWayValveMixing,
    ThreeWayValveDiverting,
)
from bob.core import (
    SCRATCH,
    BoundaryConnectionPoint,
    PropertyReference,
    System,
    logging,
)
from bob.template import template_update
from .actuator import ElectricalOnOffActuator, ElectricalProportionalActuator

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = SCRATCH


class TwoWayActuatedValve(System):
    """
    This base class allow the creation of SystemConnectionPoints
    via the config mechanism
    """

    _class_iri = SCRATCH.TwoWayActuatedValve
    fluidInlet: BoundaryConnectionPoint
    fluidOutlet: BoundaryConnectionPoint
    position: PropertyReference
    command: PropertyReference
    position_feedback: PropertyReference
    is_open: PropertyReference
    is_closed: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"TwoWayActuatedValve.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)

        self.command = self["valve"]["command"] = self["actuator"]["command"]
        self["is_open"] = self["valve"]["is_open"] = self["actuator"]["is_open"]
        self["is_closed"] = self["valve"]["is_closed"] = self["actuator"]["is_closed"]
        self["actuator"].linkageOutlet >> self["valve"].linkageInlet
        self.position = self["valve"].position = self["actuator"].position
        self["position_feedback"] = self["actuator"]["position_sensor"].observedProperty
        self.fluidInlet = self["valve"].fluidInlet
        self.fluidOutlet = self["valve"].fluidOutlet


electrical_actuated_proportional_2w_valve_template = {
    "equipment": {
        ("actuator", ElectricalProportionalActuator): {},
        ("valve", TwoWayValve): {},
    },
    "properties": {},
}


class TwoWayActuatedProportionalValve(TwoWayActuatedValve):
    _class_iri = SCRATCH.TwoWayActuatedProportionalValve

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            electrical_actuated_proportional_2w_valve_template, config
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"TwoWayActuatedProportionalValve.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)


electrical_actuated_onoff_2w_valve_template = {
    "equipment": {
        ("actuator", ElectricalOnOffActuator): {},
        ("valve", TwoWayValve): {},
    },
    "properties": {},
}


class TwoWayActuatedOnOffValve(TwoWayActuatedValve):
    _class_iri = SCRATCH.TwoWayActuatedOnOffValve

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(electrical_actuated_onoff_2w_valve_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"TwoWayActuatedOnOffValve.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)


class ThreeWayActuatedValve(System):
    """
    This base class allow the creation of SystemConnectionPoints
    via the config mechanism
    """

    _class_iri = SCRATCH.ThreeWayActuatedValve

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.command = self["valve"]["command"] = self["actuator"]["command"]
        self["is_open"] = self["valve"]["is_open"] = self["actuator"]["is_open"]
        self["is_closed"] = self["valve"]["is_closed"] = self["actuator"]["is_closed"]
        self["actuator"].linkageOutlet >> self["valve"].linkageInlet
        self["position"] = self["valve"]["position"] = self["actuator"]["position"]
        self["position_feedback"] = self["actuator"]["position_sensor"].observedProperty


class ThreeWayMixingSystem(ThreeWayActuatedValve):
    _class_iri = SCRATCH.ThreeWayMixingSystem
    fluidInletAB: BoundaryConnectionPoint
    fluidOutletA: BoundaryConnectionPoint
    fluidOutletB: BoundaryConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            {"equipment": {("valve", ThreeWayValveMixing): {}}}, config
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.fluidInletAB = self["valve"].fluidInletAB
        self.fluidOutletA = self["valve"].fluidOutletA
        self.fluidOutletB = self["valve"].fluidOutletB


class ThreeWayDivertingSystem(ThreeWayActuatedValve):
    _class_iri = SCRATCH.ThreeWayDivertingSystem
    fluidInletA: BoundaryConnectionPoint
    fluidInletB: BoundaryConnectionPoint
    fluidOutlet: BoundaryConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            {"equipment": {("valve", ThreeWayValveDiverting): {}}}, config
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.fluidInletA = self["valve"].fluidInletA
        self.fluidInletB = self["valve"].fluidInletB
        self.fluidOutlet = self["valve"].fluidOutlet


class ThreeWayMixingActuatedProportionalValve(ThreeWayMixingSystem):
    node_type = SCRATCH.ThreeWayMixingActuatedProportionalValve

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            {"equipment": {("actuator", ElectricalProportionalActuator): {}}}, config
        )
        kwargs = {**_config.get("params", {}), **kwargs}
        _log.debug(
            f"ThreeWayMixingActuatedProportionalValve.__init__ {_config} {kwargs}"
        )
        super().__init__(_config, **kwargs)


class ThreeWayMixingActuatedOnOffValve(ThreeWayValveMixing):
    _class_iri = SCRATCH.ThreeWayMixingActuatedOnOffValve

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            {"equipment": {("actuator", ElectricalOnOffActuator): {}}}, config
        )
        kwargs = {**_config.get("params", {}), **kwargs}
        _log.debug(f"ThreeWayMixingActuatedOnOffValve.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)


class ThreeWayDivertingActuatedProportionalValve(ThreeWayDivertingSystem):
    _class_iri = SCRATCH.ThreeWayDivertingActuatedProportionalValve

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            {"equipment": {("actuator", ElectricalProportionalActuator): {}}}, config
        )
        kwargs = {**_config.get("params", {}), **kwargs}
        _log.debug(
            f"ThreeWayDivertingActuatedProportionalValve.__init__ {_config} {kwargs}"
        )
        super().__init__(_config, **kwargs)


class ThreeWayDivertingActuatedOnOffValve(ThreeWayValveDiverting):
    _class_iri = SCRATCH.ThreeWayDivertingActuatedProportionalValve

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            {"equipment": {("actuator", ElectricalOnOffActuator): {}}}, config
        )
        kwargs = {**_config.get("params", {}), **kwargs}
        _log.debug(f"ThreeWayDivertingActuatedOnOffValve.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)
