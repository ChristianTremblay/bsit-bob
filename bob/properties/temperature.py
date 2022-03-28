from rdflib import URIRef

from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty
from ..core import quantitykind, unit, p223

__namespace__ = p223


class Temperature(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Temperature

    def __init__(self, unit):
        self.unit = unit
