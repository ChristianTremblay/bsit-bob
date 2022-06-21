from rdflib import URIRef

from ..core import Medium, Substance, BOB, P223, QUANTITYKIND, S223, UNIT
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = P223


class ParticulateCount(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.NumberDensity
    unit = UNIT["NUM-PER-M3"]
    ofMedium: Medium
    ofSubstance: Substance
