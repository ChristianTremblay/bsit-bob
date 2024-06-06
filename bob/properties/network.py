from rdflib import URIRef

from ..core import (
    BOB,
    P223,
    QUANTITYKIND,
    S223,
    UNIT,
    Medium,
    QuantifiableObservableProperty,
)

_namespace = BOB


class Mbit_per_seconds(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.DataRate
    hasUnit = UNIT["MegaBIT-PER-SEC"]


class Kbit_per_seconds(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.DataRate
    hasUnit = UNIT["KiloBIT-PER-SEC"]
