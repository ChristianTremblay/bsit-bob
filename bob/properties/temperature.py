from rdflib import URIRef

from ..core import p223, quantitykind, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

__namespace__ = p223


class Temperature(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Temperature

    def __init__(self, unit):
        self.unit = unit
