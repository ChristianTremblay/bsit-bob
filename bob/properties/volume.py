from rdflib import URIRef

from ..core import p223, quantitykind, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = p223


class Gallons(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.LiquidVolume
    unit: URIRef = unit.GAL_US
