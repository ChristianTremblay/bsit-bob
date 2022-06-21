from rdflib import URIRef

from ..core import Medium, BOB, P223, QUANTITYKIND, S223, UNIT
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = BOB


class Temperature(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Temperature
    unit: URIRef
    ofMedium: Medium  # set from the sensor
    # isObservedBy: Sensor
