from rdflib import URIRef

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import Device, PropertyReference, BOB, P223, S223

_namespace = BOB


class Filter(Device):
    _class_iri = S223.Filter
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint

    # Those come from sensors, but accessible from here
    differentialPressure: PropertyReference
    alarmStatus: PropertyReference
