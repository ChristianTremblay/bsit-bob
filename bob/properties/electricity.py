from rdflib import URIRef

from ..core import p223, quantitykind, unit
from ..property import QuantifiableObservableProperty

__namespace__ = p223


class Volts(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Voltage
    unit: URIRef = unit.V


class Amps(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.ElectricCurrent
    unit: URIRef = unit.A


class PowerFactor(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.PowerFactor
    unit: URIRef = unit.UNITLESS


class ElectricPowerkW(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Power
    unit: URIRef = unit.KiloW


class ElectricPowerW(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Power
    unit: URIRef = unit.W
