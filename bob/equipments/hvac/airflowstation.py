from rdflib import URIRef

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import BOB, P223, S223, Device
from ...sensor import Sensor

_namespace = BOB


class AirFlowMonitor(Device):
    _class_iri = P223.Actuator
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    flowSensor: Sensor


# TODO : Create the template and make that the same than the others.
