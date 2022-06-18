from rdflib import URIRef

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import Device, bob, p223, s223
from ...sensor import Sensor

_namespace = bob


class AirFlowMonitor(Device):
    _class_iri = p223.Actuator
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    flowSensor: Sensor


# TODO : Create the template and make that the same than the others.
