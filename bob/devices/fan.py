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


class Fan(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint



class VFDFan(Fan):
    # This could also be made more explicit by linking a VFD and a Fan
    speed = AnalogOut
    frequency = AnalogIn 