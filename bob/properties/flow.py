from rdflib import URIRef

from ..core import Medium, quantitykind, s223, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = s223


class Flow(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.VolumeFlowRate
    unit: URIRef
    ofMedium: Medium  # set from the sensor
    # isObservedBy: Sensor
