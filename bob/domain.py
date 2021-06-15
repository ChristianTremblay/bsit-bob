from rdflib import URIRef
from .core import s223, Domain

__namespace__ = s223


Electrical = Domain(node_iri=s223.Electrical)
Fire = Domain(node_iri=s223.Fire)
HVAC = Domain(node_iri=s223.HVAC)
Lighting = Domain(node_iri=s223.Lighting)
Occupancy = Domain(node_iri=s223.Occupancy)
Security = Domain(node_iri=s223.Security)
Networking = Domain(node_iri=s223.Networking)
