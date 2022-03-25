from rdflib import URIRef

from ..property import QuantifiableObservableProperty, QuantifiableProperty
from ..core import quantitykind, unit, p223
from .ratio import Percent

__namespace__ = p223


class Brightness(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Illuminance
    unit: URIRef = unit.LUX


class RelativeLuminousFlux(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.RelativeLuminousFlux
    unit: URIRef = unit.PERCENT
