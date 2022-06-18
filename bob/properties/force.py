from rdflib import URIRef

from ..core import Medium, bob, p223, quantitykind, unit
from ..property import QuantifiableObservableProperty

_namespace = bob

# all = [HP, Pressure, DifferentialStaticPressure]


class HP(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.Power
    unit = unit.HP


class Nm(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.Torque
    unit = unit["N-M"]


class Pressure(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.Pressure


class DifferentialStaticPressure(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.ForcePerArea
    unit: URIRef
    ofMedium: Medium  # set from the sensor
