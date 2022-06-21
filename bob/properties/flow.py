from rdflib import URIRef

from ..core import Medium, BOB, P223, QUANTITYKIND, S223, UNIT
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = BOB


class Flow(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.VolumeFlowRate
    unit: URIRef
    ofMedium: Medium  # set from the sensor
    # isObservedBy: Sensor
    measuresMedium: Medium  # set from the sensor
