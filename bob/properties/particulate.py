from rdflib import URIRef

from ..core import Medium, Substance, quantitykind, s223, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

__namespace__ = s223


class ParticulateCount(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.NumberDensity
    unit: URIRef = unit["NUM-PER-M3"]
    measuresMedium: Medium
    measuresSubstance: Substance
