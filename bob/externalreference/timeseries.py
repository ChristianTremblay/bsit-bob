from rdflib import Literal, URIRef

from ..core import ExternalReference, p223

_namespace = p223


class BACnetReference(ExternalReference):
    hasRef: Literal
    _class_iri =None


class NiagaraORDReference(ExternalReference):
    hasRef: Literal
    _class_iri =None


class TimeSeriesReference(ExternalReference):
    hasRef: Literal
    _class_iri =None
