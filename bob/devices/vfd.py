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
from ..connections.electricity import (
    PowerInletConnectionPoint,
    PowerOutletConnectionPoint,
)
from ..signal import AnalogIn, AnalogOut

__namespace__ = s223


class VFD(Device):
    powerInlet: PowerInletConnectionPoint
    powerOutlet: PowerOutletConnectionPoint
    actual_speed = AnalogIn  # RPM
    moter_temp = AnalogIn
    # etc
