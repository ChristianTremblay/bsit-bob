from rdflib import URIRef

from ..core import (
    BOB,
    P223,
    QUANTITYKIND,
    UNIT,
    QuantifiableObservableProperty,
)
from .ratio import Percent

_namespace = BOB


class Brightness(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Illuminance
    hasUnit = UNIT.LUX


class RelativeLuminousFlux(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.RelativeLuminousFlux
    hasUnit = UNIT.PERCENT
