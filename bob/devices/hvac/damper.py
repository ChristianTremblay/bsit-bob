from rdflib import URIRef
from ...core import s223, p223
from ...core import Device

from ...connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    AirBidirectionalConnectionPoint,
    CompressedAirConnectionPoint,
)

from ...connections.electricity import ElectricalInletConnectionPoint

from ...signal import AnalogIn, AnalogOut

__namespace__ = s223


class Damper(Device):
    node_type = s223.Damper
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint


class GravityDamper(Damper):
    node_type = s223.Damper


class FireDamper(Damper):
    node_type = s223.Damper


class ActuatedDamper(Damper):
    node_type = s223.Damper
    position = AnalogOut
    feedback = AnalogIn


class ElectricalActuatedDamper(Damper):
    node_type = s223.Damper
    position = AnalogOut
    feedback = AnalogIn
    powerInlet: ElectricalInletConnectionPoint


class PneumaticDamper(Damper):
    node_type = s223.Damper
    compressedAirInlet: CompressedAirConnectionPoint
    position = AnalogIn


class Window(Device):
    node_type = p223.Window
    indoor: AirBidirectionalConnectionPoint
    outdoor: AirBidirectionalConnectionPoint
