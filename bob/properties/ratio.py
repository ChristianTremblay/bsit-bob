from rdflib import URIRef

from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty
from ..core import quantitykind, unit, p223

__namespace__ = p223


class Percent(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.DimensionlessRatio
    unit: URIRef = unit.Percent


class PercentCommand(QuantifiableActuatableProperty):
    hasQuantityKind: URIRef = quantitykind.DimensionlessRatio
    unit: URIRef = unit.Percent


class RPM(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.AngularVolocity
    unit: URIRef = unit["REV-PER-MIN"]
