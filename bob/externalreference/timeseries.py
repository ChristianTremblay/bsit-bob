from rdflib import Literal, URIRef

from ..core import BOB, P223, S223, ExternalReference

_namespace = P223


class NiagaraORDReference(ExternalReference):
    _class_iri = None


class TimeSeriesReference(ExternalReference):
    _class_iri = None
