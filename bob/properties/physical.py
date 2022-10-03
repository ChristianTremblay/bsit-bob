from rdflib import URIRef

from ..core import BOB, P223, QUANTITYKIND, UNIT, Medium
from ..property import QuantifiableObservableProperty

_namespace = BOB

# all = [HP, Pressure, DifferentialStaticPressure]


class Length(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Length


class Area(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Area
