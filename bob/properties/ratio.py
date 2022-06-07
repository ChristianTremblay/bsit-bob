from rdflib import URIRef

from ..core import Air, Medium, Substance, p223, quantitykind, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = p223


class Percent(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.DimensionlessRatio
    unit = unit.PERCENT


class PercentCommand(QuantifiableActuatableProperty):
    hasQuantityKind = quantitykind.DimensionlessRatio
    unit = unit.PERCENT


class RPM(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.AngularVolocity
    unit = unit["REV-PER-MIN"]


class RelativeHumidity(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.RelativeHumidity
    unit = unit.PERCENT_RH
    ofMedium: Medium = Air


class GasConcentration(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.DimensionlessRatio
    unit = unit.PPM
    ofMedium: Medium = Air
    ofSubstance: Substance
