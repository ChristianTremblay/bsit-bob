from rdflib import URIRef

from ..core import Air, Medium, Substance, BOB, P223, QUANTITYKIND, S223, UNIT
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = BOB


class Percent(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.DimensionlessRatio
    unit = UNIT.PERCENT


class PercentCommand(QuantifiableActuatableProperty):
    hasQuantityKind = QUANTITYKIND.DimensionlessRatio
    unit = UNIT.PERCENT


class RPM(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.AngularVolocity
    unit = UNIT["REV-PER-MIN"]


class RelativeHumidity(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.RelativeHumidity
    unit = UNIT.PERCENT_RH
    ofMedium: Medium = Air


class GasConcentration(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.DimensionlessRatio
    unit = UNIT.PPM
    ofMedium: Medium = Air
    ofSubstance: Substance
