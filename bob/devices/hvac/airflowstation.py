from rdflib import URIRef

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import Device, p223, s223
from ...sensor import Sensor

_namespace = p223


class AirFlowMonitor(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    flowSensor: Sensor


# TODO : Create the template and make that the same than the others.
