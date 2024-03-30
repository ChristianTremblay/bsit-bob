from typing import Dict, Union

from rdflib import URIRef

from bob.connections.mechanical import MechanicalOutletConnectionPoint
from bob.enum import OpenCloseEnum
from bob.producer import Producer, ProducerInput, ProducerOutput
from bob.producer.causality import Causality
from bob.properties import Nm, Percent, PercentCommand
from bob.properties.states import OnOffCommand, OnOffStatus
from bob.sensor.motion import PositionSensor
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
    Electricity_24VLN_1Ph_60HzInletConnectionPoint,
    Electricity_120VLN_1Ph_60HzInletConnectionPoint,
)
from ...connections.controlsignal import (
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
  |   |  |   |--------s223:hasConnectionPoint-----(linkage coupling CNX  <-> G)--------hasConnectionPoint----|  Damper          |----s223:hasProperty---(mech_position) <-> A
  |   |  |   |   |----s223:hasConnectionPoint-----(Auxiliary position switch CNX) <-> F                      |  s223:Equipment  |----s223:hasProperty---(command) <-> B
  |   |  |   |   |                                                                                           |                  |----s223:hasProperty---(feedback) <-> C
  |   |  |   |   |                                                                                           |__________________|----s223:hasProperty---(other damper prop...)
__|___|__|___|___|__                                                                                  
|  Damper Actuator |------------s223:hasProperty--------(mech_position) <-> A                                   
|  s223:Equipment  |------------s223:hasProperty--------(command) <-> B
|                  |------------s223:hasProperty--------(feedback) <-> C
|                  |------------s223:hasProperty--------(is_open) <-> D1
|__________________|------------s223:hasProperty--------(is_closed) <-> D2
    |   |  |  |
    |   |  |  |
    |   |  |  |                     ____________________
    |   |  |  |___s223:contains_____|  Position Act.   |---s223:hasInput--(producer_input)--s223:uses----------(command) <-> B
    |   |  |                        |  S223:Producer   |---s223:hasOutput--(producer_output)--s223:produces-------(mech_position) <-> A
    |   |  |                        |__________________|---p223:hasEffectLocation---(mechanical coupling CNX) <-> G
    |   |  |                        ____________________
    |   |  |______s223:contains_____|  Position Observ |
    |   |                           |  s223:Sensor   |---s223:observes------------------(mech_position) <-> A
    |   |                           |__________________|---s223:hasObservationLocation----(mechanical coupling CNX) <-> G
    |   |                           ____________________
    |   |_________s223:contains_____|  Feedback Act.   |---s223:hasInput--(producer_input)--s223:uses----------(mech_position) <-> A
    |                               |  S223:Producer   |---s223:hasOutput--(producer_output)--s223:produces-------(feedback)  <-> C
    |                               |__________________|---p223:hasEffectLocation---(0-10VDC Feedback Output) <-> E
    |                               ____________________
    |___________s223:contains_______|  Aux.Sw.Act. (2x)|---s223:hasInput--(producer_input)--s223:uses----------(mech_position) <-> A
                                    |  S223:Producer   |---s223:hasOutput--(producer_output)--s223:produces-------(is_open or is_close)  <-> D1&D2
                                    |__________________|---p223:hasEffectLocation---(auxiliary position switch CNX) <-> F

    |___________s223:contains_______|  position        |---s223:hasInput--(producer_input)--s223:uses----------(feedback) <-> C
                                    |  S223:Producer   |---s223:hasOutput--(producer_output)--s223:produces-------(What Joel calls Position)
                                    |__________________|

    |___________s223:contains_______|  position        |---s223:hasInput--(producer_input)--s223:uses----------(command) <-> B
                                    |  S223:Producer   |---s223:hasOutput--(producer_output)--s223:produces-------(What Joel calls Position)
                                    |__________________|

Note : "Could" We can get rid of Observer pattern (which is hidden inside sensor) IF we can relate a property to a location in the model ?

Note2 : Producers could be Function Blocks...but I don't like that :)

Note3 : Mech_position is a property, unreachable from outside the model. It doens't provide a value. It is the intrinsic position... the value can only come from other properties through external references.
"""

BasicActuator_template = {
    "cp": {
        "linkageOutlet": MechanicalOutletConnectionPoint,
        "feedback_signal": ModulationSignalOutletConnectionPoint,
        "open_auxswitch_signal": OnOffSignalOutletConnectionPoint,
        "close_auxswitch_signal": OnOffSignalOutletConnectionPoint,
    },
    "properties": {
        ("position_feedback", Percent): {},
        ("is_open", OnOffStatus): {},
        ("is_closed", OnOffStatus): {},
    },
    "parts": {
        ("positionProducer", Causality): {},
        ("feedbackProducer", Causality): {},
        ("auxiliary_switch_open_producer", Causality): {},
        ("auxiliary_switch_close_producer", Causality): {},
        ("position_sensor", PositionSensor): {},
    },
}


class BaseActuator(Equipment):
    _class_iri = S223.Actuator
    command: Union[PercentCommand, OnOffCommand]
    position: PropertyReference
    position_feedback: Union[Percent, OpenCloseEnum]
    is_open: OnOffStatus
    is_closed: OnOffStatus

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(BasicActuator_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)

        self.position = self["position_sensor"].observedProperty
        self["position_sensor"] % self.linkageOutlet
        self["positionProducer"].cause_input << self["command"]
        self["positionProducer"].effect_output >> self.position
        self["positionProducer"].effect_output.hasEffectLocation = self.linkageOutlet

        self["feedbackProducer"].cause_input << self.position
        self["feedbackProducer"].effect_output >> self["position_feedback"]
        self["feedbackProducer"].effect_output.hasEffectLocation = self.feedback_signal

        self["auxiliary_switch_open_producer"].cause_input << self.position
        self["auxiliary_switch_open_producer"].effect_output >> self["is_open"]
        self[
            "auxiliary_switch_open_producer"
        ].effect_output.hasEffectLocation = self.open_auxswitch_signal

        self["auxiliary_switch_close_producer"].cause_input << self.position
        self["auxiliary_switch_close_producer"].effect_output >> self["is_closed"]
        self[
            "auxiliary_switch_close_producer"
        ].effect_output.hasEffectLocation = self.close_auxswitch_signal


"""
ELECTRICAL PROPORTIONAL DAMPER/VALVE ACTUATOR
"""

ElectricalProportionalActuator_template = {
    "cp": {
        "electricalInlet": Electricity_24VLN_1Ph_60HzInletConnectionPoint,
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
    _class_iri = S223.Actuator
    command: PercentCommand

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(ElectricalProportionalActuator_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self["positionProducer"].cause_input.hasCauseLocation = self.proportional_signal


"""
ELECTRICAL ON/OFF DAMPER/VALVE ACTUATOR
"""
ElectricalOnOffActuator_template = {
    "cp": {
        "electricalInlet": Electricity_24VLN_1Ph_60HzInletConnectionPoint,
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
    _class_iri = S223.Actuator
    command: OnOffCommand

    def __init__(self, config: Dict = {}, **kwargs):
        _config = template_update(ElectricalOnOffActuator_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self["positionProducer"].cause_input.hasCauseLocation = self.onoff_signal


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
    _class_iri = S223.Actuator
    compressedAirInlet: CompressedAirInletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(PneumaticProportionalActuator_template, config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self["positionProducer"].cause_input.hasCauseLocation = self.compressedAirInlet


class PneumaticOnOffActuator(BaseActuator):
    _class_iri = S223.Actuator
    compressedAirInlet: CompressedAirInletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = PneumaticOnOffActuator_template
        if config:
            _config.update(config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self["positionProducer"].cause_input.hasCauseLocation = self.compressedAirInlet
