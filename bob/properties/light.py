from rdflib import URIRef

from ..core import BOB, P223, QUANTITYKIND, UNIT
from ..property import QuantifiableObservableProperty, QuantifiableProperty
from .ratio import Percent

_namespace = BOB


class Brightness(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Illuminance
    unit = UNIT.LUX


class RelativeLuminousFlux(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.RelativeLuminousFlux
    unit = UNIT.PERCENT
