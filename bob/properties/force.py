from rdflib import URIRef

from ..core import Medium, BOB, P223, QUANTITYKIND, UNIT
from ..property import QuantifiableObservableProperty

_namespace = BOB

# all = [HP, Pressure, DifferentialStaticPressure]


class HP(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Power
    unit = UNIT.HP


class Nm(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Torque
    unit = UNIT["N-M"]


class Pressure(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Pressure


class DifferentialStaticPressure(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.ForcePerArea
    unit: URIRef
    ofMedium: Medium  # set from the sensor
