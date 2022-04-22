from rdflib import URIRef

from ...connections.air import CompressedAirOutletConnectionPoint
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)
from ...core import Device, p223, s223
from ...signal import AnalogIn, AnalogOut

_namespace = p223


class AirCompressor(Device):
    node_type: URIRef = p223.AirCompressor
    compressedAirOutlet: CompressedAirOutletConnectionPoint
    electricalInlet: ElectricalInletConnectionPoint
