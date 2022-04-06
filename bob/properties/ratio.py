from rdflib import URIRef

from ..core import p223, quantitykind, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

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
