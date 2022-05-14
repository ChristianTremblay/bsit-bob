from rdflib import URIRef

from ..core import Medium, p223, quantitykind, unit
from ..property import QuantifiableObservableProperty

_namespace = p223

# all = [HP, Pressure, DifferentialStaticPressure]


class HP(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Power
    unit: URIRef = unit.HP


class Nm(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Torque
    unit: URIRef = unit["N-M"]


class Pressure(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Pressure


class DifferentialStaticPressure(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.ForcePerArea
    unit: URIRef
    ofMedium: Medium  # set from the sensor
