from rdflib import URIRef

from ..core import p223, quantitykind, unit
from ..property import QuantifiableObservableProperty

__namespace__ = p223


class HP(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Power
    unit: URIRef = unit.HP


class Pressure(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Pressure

    def __init__(self, unit):
        self.unit = unit
