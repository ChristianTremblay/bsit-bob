from rdflib import URIRef

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import BOB, P223, S223, Equipment
from ...sensor import Sensor

_namespace = BOB


class AirFlowMonitor(Equipment):
    _class_iri = P223.AirFlowMonitor
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    flowSensor: Sensor


# TODO : Create the template and make that the same than the others.
