from rdflib import URIRef
from ..core import (
    s223,
    Substance,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    SystemConnectionPoint,
    InletSystemConnectionPoint,
    OutletSystemConnectionPoint,
    Device,
)
from ..connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint
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