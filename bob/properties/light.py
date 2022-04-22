from rdflib import URIRef

from ..core import p223, quantitykind, unit
from ..property import QuantifiableObservableProperty, QuantifiableProperty
from .ratio import Percent

_namespace = p223


class Brightness(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Illuminance
    unit: URIRef = unit.LUX


class RelativeLuminousFlux(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.RelativeLuminousFlux
    unit: URIRef = unit.PERCENT
