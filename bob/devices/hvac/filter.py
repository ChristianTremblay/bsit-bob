from rdflib import URIRef
from ...core import s223, Device
from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...signal import AnalogIn, AnalogOut

__namespace__ = s223


class Filter(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    dp = AnalogOut
