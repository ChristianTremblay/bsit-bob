from rdflib import URIRef

from ..core import BOB, P223, QUANTITYKIND, S223, UNIT, Medium
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = BOB


class Mbit_per_seconds(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.DataRate
    unit = UNIT["MegaBIT-PER-SEC"]


class Kbit_per_seconds(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.DataRate
    unit = UNIT["KiloBIT-PER-SEC"]
