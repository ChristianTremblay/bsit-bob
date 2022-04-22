from rdflib import URIRef

from .core import Role, s223

_namespace = s223


Exhaust = Role(node_iri=s223.Exhaust)
Primary = Role(node_iri=s223.Primary)
Secondary = Role(node_iri=s223.Secondary)
Supply = Role(node_iri=s223.Supply)
Return = Role(node_iri=s223.Return)
