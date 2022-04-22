from rdflib import URIRef

from ..core import Air, Medium, Substance, p223, quantitykind, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = p223


class Percent(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.DimensionlessRatio
    unit: URIRef = unit.Percent


class PercentCommand(QuantifiableActuatableProperty):
    hasQuantityKind: URIRef = quantitykind.DimensionlessRatio
    unit: URIRef = unit.Percent


class RPM(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.AngularVolocity
    unit: URIRef = unit["REV-PER-MIN"]


class RelativeHumidity(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.RelativeHumidity
    unit: URIRef = unit.PERCENT_RH
    measuresMedium: Medium = Air


class GasConcentration(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.DimensionlessRatio
    unit: URIRef = unit.PPM
    measuresMedium: Medium = Air
    measuresSubstance: Substance
