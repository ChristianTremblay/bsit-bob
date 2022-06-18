from rdflib import URIRef

from ..core import Medium, bob, p223, quantitykind, s223, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = bob


class Temperature(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.Temperature
    unit: URIRef
    ofMedium: Medium  # set from the sensor
    # isObservedBy: Sensor
