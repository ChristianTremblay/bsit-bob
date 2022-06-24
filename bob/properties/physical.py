from rdflib import URIRef

from ..core import Medium, BOB, P223, QUANTITYKIND, UNIT
from ..property import QuantifiableObservableProperty

_namespace = BOB

# all = [HP, Pressure, DifferentialStaticPressure]


class Length(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Length


class Area(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Area
