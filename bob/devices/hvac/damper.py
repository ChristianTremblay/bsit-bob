from rdflib import URIRef

from ...connections.air import (
    AirBidirectionalConnectionPoint,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    CompressedAirConnectionPoint,
    CompressedAirInletConnectionPoint,
)
from ...connections.electricity import ElectricalInletConnectionPoint
from ...connections.light import (
    LightOutletConnectionPoint,
    LightVisibleOutletConnectionPoint,
)
from ...core import Device, p223, s223
from ...signal import AnalogIn, AnalogOut

_namespace = s223


class DamperActuator(Device):
    _class_iri = s223.DamperActuator
    position = AnalogOut
    feedback = AnalogIn


class ElectricalDamperActuator(Device):
    _class_iri = s223.DamperActuator
    electricalInlet: ElectricalInletConnectionPoint
    position = AnalogOut
    feedback = AnalogIn


class PneumaticDamperActuator(Device):
    _class_iri = s223.DamperActuator
    compressedAirInlet: CompressedAirInletConnectionPoint
    position = AnalogOut
    feedback = AnalogIn


class Damper(Device):
    _class_iri = s223.Damper
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    position = AnalogOut
    feedback = AnalogIn


class GravityDamper(Damper):
    _class_iri = s223.Damper


class FireDamper(Damper):
    _class_iri = s223.Damper


class ActuatedDamper(Damper):
    _class_iri = s223.Damper


class ElectricalActuatedDamper(Damper):
    _class_iri = s223.Damper
    powerInlet: ElectricalInletConnectionPoint


class PneumaticDamper(Damper):
    _class_iri = s223.Damper
    compressedAirInlet: CompressedAirConnectionPoint


class Window(Device):
    _class_iri = p223.Window
    indoor: AirBidirectionalConnectionPoint
    outdoor: AirBidirectionalConnectionPoint
    naturalLight: LightVisibleOutletConnectionPoint
