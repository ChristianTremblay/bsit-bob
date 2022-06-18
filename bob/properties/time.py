from rdflib import URIRef

from ..core import Medium, bob, p223, quantitykind, s223, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = bob


class Hour(QuantifiableObservableProperty):
    _class_iri = p223.Hour
    hasQuantityKind = quantitykind.Time
    unit: URIRef = unit.HR


class Minute(QuantifiableObservableProperty):
    _class_iri = p223.Minute
    hasQuantityKind = quantitykind.Time
    unit: URIRef = unit.MIN
