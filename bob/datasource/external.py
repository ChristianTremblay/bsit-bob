from rdflib import URIRef
from ..core import (
    s223,
)

__namespace__ = s223


class ExternalDataSource:
    pass


class BACnetDataSource(ExternalDataSource):
    hasExternalDataSource: URIRef
    node_type = None
