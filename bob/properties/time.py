from rdflib import URIRef

from ..core import Medium, quantitykind, s223, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = s223


class Hour(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.Time
    unit: URIRef = unit.HR


class Minute(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.Time
    unit: URIRef = unit.MIN
