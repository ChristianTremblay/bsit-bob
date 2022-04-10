from rdflib import URIRef

from ..core import Medium, quantitykind, s223, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

__namespace__ = s223


class Flow(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.VolumeFlowRate
    unit: URIRef
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor
