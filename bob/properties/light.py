from rdflib import URIRef

from ..property import QuantifiableObservableProperty, QuantifiableProperty
from ..core import quantitykind, unit, p223
from .ratio import Percent

__namespace__ = p223


class Brightness(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.Illuminance
    unit: URIRef = unit.LUX
