from rdflib import URIRef

from ..core import BOB, P223, QUANTITYKIND, S223, UNIT, Medium
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = BOB


class Gallons(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.LiquidVolume
    unit = UNIT.GAL_US
    measuresMedium: Medium  # set from the sensor
