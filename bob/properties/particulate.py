from rdflib import URIRef
from typing import Union
from ..core import (
    BOB,
    P223,
    QUANTITYKIND,
    S223,
    UNIT,
    Medium,
    Substance,
    Constituent,
    QuantifiableObservableProperty,
)

_namespace = P223


class ParticulateCount(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.NumberDensity
    hasUnit = UNIT["NUM-PER-M3"]
    ofMedium: Medium
    ofSubstance: Substance
