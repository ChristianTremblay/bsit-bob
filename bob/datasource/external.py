from rdflib import URIRef
from ..core import (
    s223,
)
from ..core import ExternalReference

__namespace__ = s223


class BACnetReference(ExternalReference):
    hasExternalReference: URIRef
    node_type = None


class NiagaraORDRefrence(ExternalReference):
    hasExternalReference: URIRef
    node_type = None
