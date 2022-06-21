from rdflib import XSD, Literal, URIRef

from ..core import EnumerationKind, Node, BOB, P223, S223
from ..property import QuantifiableProperty

_namespace = BOB


class Setpoint(QuantifiableProperty):
    _class_iri: URIRef = S223.Setpoint
    hasApsect: EnumerationKind
    hasDeadband: Literal
    hasValue: Literal
    hasQuantityKind: URIRef
    unit: URIRef

    def __init__(self, **kwargs):
        _properties = {}
        for k, v in self.__annotations__.items():
            if k in kwargs:
                _properties[k] = kwargs.pop(k)
        super().__init__(**kwargs)
        for k, v in _properties.items():
            if v is not None:
                setattr(self, k, self.__annotations__[k](v))
