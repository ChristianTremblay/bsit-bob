from rdflib import URIRef

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import BOB, P223, S223, Equipment, PropertyReference

_namespace = BOB


class Filter(Equipment):
    _class_iri = P223.Filter
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint

    # Those come from sensors, but accessible from here
    differentialPressure: PropertyReference
    alarmStatus: PropertyReference
