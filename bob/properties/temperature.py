from rdflib import URIRef

from ..core import Medium, p223, quantitykind, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = p223


class Temperature(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Temperature
    unit: URIRef
    ofMedium: Medium  # set from the sensor
    # isObservedBy: Sensor
