from rdflib import URIRef

from ..core import BOB, P223, QUANTITYKIND, S223, UNIT, Medium
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = BOB


class DifferentialTime(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Time


class Hour(DifferentialTime):
    hasUnit: URIRef = UNIT.HR


class Minute(DifferentialTime):
    hasUnit: URIRef = UNIT.MIN


class Second(DifferentialTime):
    hasUnit: URIRef = UNIT.SEC
