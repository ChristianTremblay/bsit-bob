from rdflib import URIRef

from ..property import QuantifiableObservableProperty
from ..core import quantitykind, unit, p223

__namespace__ = p223


class HP(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Power
    unit: URIRef = unit.HP
