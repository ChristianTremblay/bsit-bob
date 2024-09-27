from rdflib import URIRef

from ..core import (
    BOB,
    P223,
    QUANTITYKIND,
    S223,
    UNIT,
    Medium,
    QuantifiableObservableProperty,
)
from ..enum import Fluid

_namespace = BOB


class Flow(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.VolumeFlowRate
    hasUnit: URIRef
    ofMedium: Fluid  # set from the sensor
    # isObservedBy: Sensor
    measuresMedium: Fluid  # set from the sensor
