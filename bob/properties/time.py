from rdflib import URIRef

from ..core import BOB, P223, QUANTITYKIND, S223, UNIT, Medium
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = BOB


class Hour(QuantifiableObservableProperty):
    _class_iri = P223.Hour
    hasQuantityKind = QUANTITYKIND.Time
    unit: URIRef = UNIT.HR


class Minute(QuantifiableObservableProperty):
    _class_iri = P223.Minute
    hasQuantityKind = QUANTITYKIND.Time
    unit: URIRef = UNIT.MIN
