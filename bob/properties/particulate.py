from rdflib import URIRef

from ..core import Medium, Substance, quantitykind, s223, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = s223


class ParticulateCount(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.NumberDensity
    unit = unit["NUM-PER-M3"]
    ofMedium: Medium
    ofSubstance: Substance
