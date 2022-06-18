from rdflib import URIRef

from ..core import Medium, bob, p223, quantitykind, s223, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = bob


class Gallons(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.LiquidVolume
    unit = unit.GAL_US
    measuresMedium: Medium  # set from the sensor
