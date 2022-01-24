from rdflib import URIRef
from ..core import (
    s223,
)
from ..node import Device

from ..connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    CompressedAirConnectionPoint,
)
from ..signal import AnalogIn, AnalogOut

__namespace__ = s223


class Damper(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint


class GravityDamper(Damper):
    pass


class FireDamper(Damper):
    pass


class ActuatedDamper(Damper):
    position = AnalogOut
    feedback = AnalogIn


class PneumaticDamper(Damper):
    compressedAirInlet: CompressedAirConnectionPoint
    position = AnalogIn
