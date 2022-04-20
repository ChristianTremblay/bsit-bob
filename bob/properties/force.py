from rdflib import URIRef

from ..core import Medium, p223, quantitykind, unit
from ..property import QuantifiableObservableProperty

_namespace = p223

# all = [HP, Pressure, DifferentialStaticPressure]


class HP(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Power
    unit: URIRef = unit.HP


class Pressure(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Pressure

    def __init__(self, unit):
        self.unit = unit


class DifferentialStaticPressure(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.ForcePerArea
    unit: URIRef
    measuresMedium: Medium  # set from the sensor
