from rdflib import URIRef
from ...core import s223, p223
from ...core import Device

from ...connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    AirBidirectionalConnectionPoint,
    CompressedAirConnectionPoint,
    CompressedAirInletConnectionPoint,
)
from ...connections.light import (
    LightOutletConnectionPoint,
    LightVisibleOutletConnectionPoint,
)

from ...connections.electricity import ElectricalInletConnectionPoint

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
