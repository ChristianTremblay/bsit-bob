from rdflib import URIRef
from ..core import (
    s223,
)
from ..node import ExternalDataSource

__namespace__ = s223


class BACnetDataSource(ExternalDataSource):
    hasExternalDataSource: URIRef
    node_type = None


class NiagaraORDDataSource(ExternalDataSource):
    hasExternalDataSource: URIRef
    node_type = None
