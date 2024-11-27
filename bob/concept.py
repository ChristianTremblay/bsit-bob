from rdflib import Graph, URIRef

from .core import (
    BOB,
    G36,
    P223,
    QUANTITYKIND,
    QUDT,
    S223,
    UNIT,
    Constituent,
    Domain,
    EnumerationKind,
    Medium,
    Mix,
    Node,
    Role,
    Substance,
)

_namespace = S223


class System_AirHandlingUnit(Node):
    _class_iri: URIRef = S223["System-AirHandlingUnit"]


class System_FanCoilUnit(Node):
    _class_iri: URIRef = S223["System-FanCoilUnit"]
