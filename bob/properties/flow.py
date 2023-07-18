from rdflib import URIRef

from ..core import BOB, P223, QUANTITYKIND, S223, UNIT, Medium
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = BOB


class Flow(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.VolumeFlowRate
    hasUnit: URIRef
    ofMedium: Medium  # set from the sensor
    # isObservedBy: Sensor
    measuresMedium: Medium  # set from the sensor
