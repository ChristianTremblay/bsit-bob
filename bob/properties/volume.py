from rdflib import URIRef

from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty
from ..core import quantitykind, unit, p223

__namespace__ = p223


class Gallons(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.LiquidVolume
    unit: URIRef = unit.GAL_US
