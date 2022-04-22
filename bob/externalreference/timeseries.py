from rdflib import Literal, URIRef

from ..core import ExternalReference, p223

_namespace = p223


class BACnetReference(ExternalReference):
    hasRef: Literal
    node_type = None


class NiagaraORDReference(ExternalReference):
    hasRef: Literal
    node_type = None


class TimeSeriesReference(ExternalReference):
    hasRef: Literal
    node_type = None
