from rdflib import URIRef

from ..core import p223, quantitykind, unit
from ..property import QuantifiableObservableProperty

_namespace = p223


class Volts(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.Voltage
    unit = unit.V


class Amps(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.ElectricCurrent
    unit = unit.A


class PowerFactor(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.PowerFactor
    unit = unit.UNITLESS


class ElectricPowerkW(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.Power
    unit = unit.KiloW


class ElectricPowerW(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.Power
    unit = unit.W
