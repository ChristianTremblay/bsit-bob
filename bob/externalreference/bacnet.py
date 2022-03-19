from rdflib import URIRef, Literal

from ..core import (
    ExternalReference,
    p223,
    ref,
    bacnet,
    EnumerationKind,
    Graph,
    schema_graph,
)

__namespace__ = p223


class BacnetProperty(EnumerationKind):
    _data_graph: Graph = schema_graph


BACnetObjectID = BacnetProperty(node_iri=bacnet["object-identifier"])
BACnetObjectOf = BacnetProperty(node_iri=bacnet["BACnetDevice"])
BacnetObjectName = BacnetProperty(node_iri=bacnet["object-name"])
BACnetDescription = BacnetProperty(node_iri=bacnet["description"])
BACnetObjectType = BacnetProperty(node_iri=bacnet["object-type"])
BACnetURI = BacnetProperty(node_iri=bacnet["BACnetURI"])


class BACnetReference(ExternalReference):
    node_type: URIRef = ref.BacnetReference
    objectId: BACnetObjectID
    objectOf: BACnetObjectOf
    objectName: BacnetObjectName
    description: BACnetDescription
    objectType: BACnetObjectType
    uri: BACnetURI
