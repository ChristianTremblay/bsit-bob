from rdflib import URIRef

from bob.connections.electricity import ElectricalInletConnectionPoint
from ...core import s223, Device


from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...signal import AnalogIn, AnalogOut

__namespace__ = s223


class Fan(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    electricalInlet: ElectricalInletConnectionPoint  # can come from a VFD
