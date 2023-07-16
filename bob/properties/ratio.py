from rdflib import URIRef

from ..core import BOB, P223, QUANTITYKIND, S223, UNIT, Air, Medium, Substance
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = BOB


class Percent(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.DimensionlessRatio
    hasUnit = UNIT.PERCENT


class PercentCommand(QuantifiableActuatableProperty):
    hasQuantityKind = QUANTITYKIND.DimensionlessRatio
    hasUnit = UNIT.PERCENT


class RPM(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.AngularVelocity
    hasUnit = UNIT["REV-PER-MIN"]


class RelativeHumidity(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.RelativeHumidity
    hasUnit = UNIT.PERCENT_RH
    ofMedium: Medium = Air


class GasConcentration(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.DimensionlessRatio
    hasUnit = UNIT.PPM
    ofMedium: Medium = Air
    ofSubstance: Substance
