from rdflib import URIRef

from ..core import Medium, quantitykind, s223, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = s223


class Mbit_per_seconds(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.DataRate
    unit = unit["MegaBIT-PER-SEC"]


class Kbit_per_seconds(QuantifiableObservableProperty):
    hasQuantityKind = quantitykind.DataRate
    unit = unit["KiloBIT-PER-SEC"]
