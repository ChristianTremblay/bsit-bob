from rdflib import URIRef
from ...core import s223, p223, Device

from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)
from ...connections.air import CompressedAirOutletConnectionPoint

from ...signal import AnalogIn, AnalogOut

__namespace__ = p223


class AirCompressor(Device):
    node_type: URIRef = p223.AirCompressor
    compressedAirOutlet: CompressedAirOutletConnectionPoint
    electricalInlet: ElectricalInletConnectionPoint
