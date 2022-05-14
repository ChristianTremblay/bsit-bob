from rdflib import URIRef

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import Device, PropertyReference, p223, s223

_namespace = p223


class Filter(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint

    # Those come from sensors, but accessible from here
    differentialPressure: PropertyReference
    alarmStatus: PropertyReference
