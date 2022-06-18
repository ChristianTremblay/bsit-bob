from rdflib import URIRef

from ..core import bob, p223, quantitykind, unit
from ..property import QuantifiableObservableProperty, QuantifiableProperty
from .ratio import Percent

_namespace = bob


class Brightness(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.Illuminance
    unit = unit.LUX


class RelativeLuminousFlux(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.RelativeLuminousFlux
    unit = unit.PERCENT
