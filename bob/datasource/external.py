from rdflib import URIRef, Literal

from ..core import ExternalReference, p223

__namespace__ = p223


class BACnetReference(ExternalReference):
    hasRef: Literal
    node_type = None


class NiagaraORDReference(ExternalReference):
    hasRef: Literal
    node_type = None


class TimeSeriesReference(ExternalReference):
    hasRef: Literal
    node_type = None
