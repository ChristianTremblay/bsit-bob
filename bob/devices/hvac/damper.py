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

__namespace__ = s223


class DamperActuator(Device):
    node_type = s223.DamperActuator
    position = AnalogOut
    feedback = AnalogIn


class ElectricalDamperActuator(Device):
    node_type = s223.DamperActuator
    electricalInlet: ElectricalInletConnectionPoint
    position = AnalogOut
    feedback = AnalogIn


class PneumaticDamperActuator(Device):
    node_type = s223.DamperActuator
    compressedAirInlet: CompressedAirInletConnectionPoint
    position = AnalogOut
    feedback = AnalogIn


class Damper(Device):
    node_type = s223.Damper
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    position = AnalogOut
    feedback = AnalogIn


class GravityDamper(Damper):
    node_type = s223.Damper


class FireDamper(Damper):
    node_type = s223.Damper


class ActuatedDamper(Damper):
    node_type = s223.Damper


class ElectricalActuatedDamper(Damper):
    node_type = s223.Damper
    powerInlet: ElectricalInletConnectionPoint


class PneumaticDamper(Damper):
    node_type = s223.Damper
    compressedAirInlet: CompressedAirConnectionPoint


class Window(Device):
    node_type = p223.Window
    indoor: AirBidirectionalConnectionPoint
    outdoor: AirBidirectionalConnectionPoint
    naturalLight: LightVisibleOutletConnectionPoint
