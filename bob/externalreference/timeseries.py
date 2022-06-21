from rdflib import Literal, URIRef

from ..core import ExternalReference, BOB, P223, S223

_namespace = P223


class BACnetReference(ExternalReference):
    hasRef: Literal
    _class_iri = None


class NiagaraORDReference(ExternalReference):
    hasRef: Literal
    _class_iri = None


class TimeSeriesReference(ExternalReference):
    hasRef: Literal
    _class_iri = None
