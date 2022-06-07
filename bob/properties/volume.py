from rdflib import URIRef

from ..core import Medium, p223, quantitykind, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = p223


class Gallons(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.LiquidVolume
    unit = unit.GAL_US
    measuresMedium: Medium  # set from the sensor
