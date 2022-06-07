from rdflib import URIRef

from ..core import Medium, p223, quantitykind, unit
from ..property import QuantifiableObservableProperty

_namespace = p223

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
