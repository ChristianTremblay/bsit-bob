from rdflib import URIRef, Literal
from typing import Any
from ..core import (
    Device,
    ExternalReference,
    Node,
    p223,
    ref,
    bacnet,
    EnumerationKind,
    Graph,
    schema_graph,
)

__namespace__ = p223


class BACnetProperty(Node):
    node_type: URIRef = bacnet.Property
    hasValue: Literal

    def __init__(self, value: Any = None, **kwargs: Any):
        init_value = None
        if value is None:
            if "hasValue" in kwargs:
                init_value = kwargs.pop("hasValue")
        elif "hasValue" in kwargs:
            raise RuntimeError("initialization conflict")
        else:
            init_value = value
        super().__init__(**kwargs)
        if init_value is not None:
            if not isinstance(init_value, Literal):
                init_value = Literal(init_value)
            self.hasValue = init_value


class BACnetDeviceId(BACnetProperty):
    node_type: URIRef = bacnet["device-identifier"]


class BACnetDeviceName(BACnetProperty):
    node_type: URIRef = bacnet["device-name"]


class BACnetNetworkNumber(BACnetProperty):
    node_type: URIRef = bacnet["network-number"]


class BACnetAddress(BACnetProperty):
    node_type: URIRef = bacnet["address"]


class BACnetVendorId(BACnetProperty):
    node_type: URIRef = bacnet["vendor-id"]


class BACnetObjectInstance(BACnetProperty):
    node_type: URIRef = bacnet["object-instance"]


class BACnetObjectOf(BACnetProperty):
    node_type: URIRef = bacnet["BACnetDevice"]


class BACnetObjectName(BACnetProperty):
    node_type: URIRef = bacnet["object-name"]


class BACnetDescription(BACnetProperty):
    node_type: URIRef = bacnet["description"]


class BACnetObjectType(BACnetProperty):
    node_type: URIRef = bacnet["object-type"]


class BACnetURI(BACnetProperty):
    node_type: URIRef = bacnet["BACnetURI"]


class BACnetDevice(Node):
    node_type: URIRef = bacnet.BACnetDevice
    deviceId: BACnetDeviceId
    deviceName: BACnetDeviceName
    networkNumber: BACnetNetworkNumber
    address: BACnetAddress
    vendorId: BACnetVendorId
    uri: BACnetURI


class BACnetReference(ExternalReference):
    node_type: URIRef = ref.BACnetReference
    objectInstance: BACnetObjectInstance
    objectOf: BACnetObjectOf
    objectName: BACnetObjectName
    description: BACnetDescription
    objectType: BACnetObjectType
    uri: BACnetURI
