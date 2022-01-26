from rdflib import URIRef
from ...core import (
    s223,
)

from ...node import Device
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)
from ...signal import AnalogIn, AnalogOut

__namespace__ = s223


class VFD(Device):
    electricalInlet: ElectricalInletConnectionPoint
    electricalOutlet: ElectricalOutletConnectionPoint
    actual_speed = AnalogIn  # RPM
    moter_temp = AnalogIn
    # etc
