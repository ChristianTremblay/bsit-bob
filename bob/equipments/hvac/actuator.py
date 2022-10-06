from typing import Dict, Union

from rdflib import URIRef

from bob.connections.mechanical import MechanicalOutletConnectionPoint
from bob.enum import OpenCloseEnum
from bob.properties import Nm, Percent, PercentCommand
from bob.properties.states import OnOffCommand, OnOffStatus
from bob.sensor.sensor import Sensor

from ...connections.air import (
    AirBidirectionalConnectionPoint,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    CompressedAirConnectionPoint,
    CompressedAirInletConnectionPoint,
    CompressedAirOutletConnectionPoint,
)
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    Electricity_24V_60HzInletConnectionPoint,
    Electricity_120V_60HzInletConnectionPoint,
    ModulationSignalInletConnectionPoint,
    ModulationSignalOutletConnectionPoint,
    OnOffSignalInletConnectionPoint,
    OnOffSignalOutletConnectionPoint,
)
from ...connections.light import (
    LightOutletConnectionPoint,
    LightVisibleOutletConnectionPoint,
)
from ...core import (
    BOB,
    P223,
    S223,
    Equipment,
    Property,
    PropertyReference,
    template_update,
)
from .. import _Actuator

_namespace = BOB

# VALVE AND DAMPER ACTUATORS

"""
  |-------------------s223:hasConnectionPoint-----(24VAC electricalInput CNX)
  |   |---------------s223:hasConnectionPoint-----(0-10VDC Feedback Output) <-> E
  |   |  |------------s223:hasConnectionPoint-----(0-10VDC Modulation signal CNX) <-> H                      ____________________
  |   |  |   |--------s223:hasConnectionPoint-----(linkage coupling CNX  <-> G)--------hasConnectionPoint----|  Damper          |----s223:hasProperty---(position) <-> A
  |   |  |   |   |----s223:hasConnectionPoint-----(Auxiliary position switch CNX) <-> F                      |  s223:Equipment     |----s223:hasProperty---(command) <-> B
  |   |  |   |   |                                                                                           |                  |----s223:hasProperty---(feedback) <-> C
  |   |  |   |   |                                                                                           |__________________|----s223:hasProperty---(other damper prop...)
__|___|__|___|___|__                                                                                  
|  Damper Actuator |------------s223:hasProperty--------(position) <-> A                                   
|  s223:Equipment     |------------s223:hasProperty--------(command) <-> B
|                  |------------s223:hasProperty--------(feedback) <-> C
|                  |------------s223:hasProperty--------(is_open) <-> D1
|__________________|------------s223:hasProperty--------(is_closed) <-> D2
    |   |  |  |
    |   |  |  |
    |   |  |  |                     ____________________
    |   |  |  |___s223:contains_____|  Position Act.   |---s223:isCommandedBy----------(command) <-> B
    |   |  |                        |  P223:Actuator   |---p223:actuatesProperty-------(position) <-> A
    |   |  |                        |__________________|---p223:hasActuationLocation---(mechanical coupling CNX) <-> G
    |   |  |                        ____________________
    |   |  |______s223:contains_____|  Position Sensor |
    |   |                           |  s223:Sensor     |---s223:observesProperty----------(position) <-> A
    |   |                           |__________________|---s223:hasMeasurementLocation----(mechanical coupling CNX) <-> G
    |   |                           ____________________
    |   |_________s223:contains_____|  Feedback Act.   |---s223:isCommandedBy----------(position) <-> A
    |                               |  P223:Actuator   |---p223:actuatesProperty-------(feedback)  <-> C
    |                               |__________________|---p223:hasActuationLocation---(0-10VDC Feedback Output) <-> E
    |                               ____________________
    |___________s223:contains_______|  Aux.Sw.Act. (2x)|---s223:isCommandedBy----------(position) <-> A
                                    |  P223:Actuator   |---p223:actuatesProperty-------(is_open or is_close)  <-> D1&D2
                                    |__________________|---p223:hasActuationLocation---(auxiliary position switch CNX) <-> F

"""

BasicActuator_template = {
    "cp": {
        "linkageOutlet": MechanicalOutletConnectionPoint,
        "feedback_signal": ModulationSignalOutletConnectionPoint,
        "open_auxswitch_signal": OnOffSignalOutletConnectionPoint,
        "close_auxswitch_signal": OnOffSignalOutletConnectionPoint,
    },
    "properties": {
        ("position", Percent): {},
        ("position_feedback", Percent): {},
        ("is_open", OnOffStatus): {},
        ("is_closed", OnOffStatus): {},
    },
    "parts": {
        ("positionActuator", _Actuator): {},
        ("feedbackActuator", _Actuator): {},
        ("auxiliary_switch_open_actuator", _Actuator): {},
        ("auxiliary_switch_close_actuator", _Actuator): {},
        ("position_sensor", Sensor): {},
    },
}


class BaseActuator(Equipment):
    _class_iri = S223.Equipment
    command: Union[PercentCommand, OnOffCommand]
    position: Percent
    position_feedback: Union[Percent, OpenCloseEnum]
    is_open: OnOffStatus
    is_closed: OnOffStatus

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(BasicActuator_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self["positionActuator"].isCommandedBy = self["command"]
        self["positionActuator"].actuatesProperty = self["position"]
        self["positionActuator"].hasActuationLocation = self.linkageOutlet

        self["feedbackActuator"].isCommandedBy = self["position"]
        self["feedbackActuator"].actuatesProperty = self["position_feedback"]
        self["feedbackActuator"].hasActuationLocation = self.feedback_signal

        self["auxiliary_switch_open_actuator"].isCommandedBy = self["position"]
        self["auxiliary_switch_open_actuator"].actuatesProperty = self["is_open"]
        self[
            "auxiliary_switch_open_actuator"
        ].hasActuationLocation = self.open_auxswitch_signal

        self["auxiliary_switch_close_actuator"].isCommandedBy = self["position"]
        self["auxiliary_switch_close_actuator"].actuatesProperty = self["is_closed"]
        self[
            "auxiliary_switch_close_actuator"
        ].hasActuationLocation = self.close_auxswitch_signal

        self["position_sensor"].observesProperty = self["position"]
        self["position_sensor"].hasMeasurementLocation = self.linkageOutlet


"""
ELECTRICAL PROPORTIONAL DAMPER/VALVE ACTUATOR
"""

ElectricalProportionalActuator_template = {
    "cp": {
        "electricalInlet": Electricity_24V_60HzInletConnectionPoint,
        "proportional_signal": ModulationSignalInletConnectionPoint,
    },
    "properties": {
        ("command", PercentCommand): {},
        ("position_feedback", Percent): {},
        ("is_open", OnOffStatus): {},
        ("is_closed", OnOffStatus): {},
        ("torque", Nm): {},
    },
}


class ElectricalProportionalActuator(BaseActuator):
    _class_iri = S223.Equipment
    command: PercentCommand

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(ElectricalProportionalActuator_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


"""
ELECTRICAL ON/OFF DAMPER/VALVE ACTUATOR
"""
ElectricalOnOffActuator_template = {
    "cp": {
        "electricalInlet": Electricity_24V_60HzInletConnectionPoint,
        "onoff_signal": OnOffSignalInletConnectionPoint,
    },
    "properties": {
        # ("actuatesProperty", OnOffCommand): {},
        ("command", OnOffCommand): {},
        ("position_feedback", Percent): {},
        ("is_open", OnOffStatus): {},
        ("is_closed", OnOffStatus): {},
        ("torque", Nm): {},
    },
}


class ElectricalOnOffActuator(BaseActuator):
    _class_iri = S223.Equipment
    command: OnOffCommand

    def __init__(self, config: Dict = {}, **kwargs):
        _config = template_update(ElectricalOnOffActuator_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


PneumaticProportionalActuator_template = {
    "cp": {},
    "properties": {
        ("command", PercentCommand): {},
        ("position_feedback", Percent): {},
        ("is_open", OnOffStatus): {},
        ("is_closed", OnOffStatus): {},
        ("torque", Nm): {},
    },
}

PneumaticOnOffActuator_template = {
    "cp": {},
    "properties": {
        # ("actuatesProperty", OnOffCommand): {},
        ("command", OnOffCommand): {},
        ("position_feedback", Percent): {},
        ("is_open", OnOffStatus): {},
        ("is_closed", OnOffStatus): {},
        ("torque", Nm): {},
    },
}


class PneumaticProportionalActuator(BaseActuator):
    _class_iri = S223.Equipment
    compressedAirInlet: CompressedAirInletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(PneumaticProportionalActuator_template, config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)


class PneumaticOnOffActuator(BaseActuator):
    _class_iri = S223.Equipment
    compressedAirInlet: CompressedAirInletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = PneumaticOnOffActuator_template
        if config:
            _config.update(config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
