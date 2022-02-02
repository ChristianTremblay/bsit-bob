from rdflib import URIRef
from ...core import (
    s223,
)
from ...core import Device

from ...connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    CompressedAirConnectionPoint,
)

from ...connections.electricity import ElectricalInletConnectionPoint

from ...signal import AnalogIn, AnalogOut

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


class ElectricalActuatedDamper(Damper):
    position = AnalogOut
    feedback = AnalogIn
    powerInlet: ElectricalInletConnectionPoint


class PneumaticDamper(Damper):
    compressedAirInlet: CompressedAirConnectionPoint
    position = AnalogIn
