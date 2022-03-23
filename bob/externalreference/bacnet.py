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


class BacnetProperty(Node):
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


class BACnetDeviceId(BacnetProperty):
    node_type: URIRef = bacnet["device-identifier"]


class BacnetDeviceName(BacnetProperty):
    node_type: URIRef = bacnet["device-name"]


class BacnetNetworkNumber(BacnetProperty):
    node_type: URIRef = bacnet["network-number"]


class BACnetAdress(BacnetProperty):
    node_type: URIRef = bacnet["address"]


class BACnetVendorId(BacnetProperty):
    node_type: URIRef = bacnet["vendor-id"]


class BACnetObjectInstance(BacnetProperty):
    node_type: URIRef = bacnet["object-instance"]


class BACnetObjectOf(BacnetProperty):
    node_type: URIRef = bacnet["BACnetDevice"]


class BacnetObjectName(BacnetProperty):
    node_type: URIRef = bacnet["object-name"]


class BACnetDescription(BacnetProperty):
    node_type: URIRef = bacnet["description"]


class BACnetObjectType(BacnetProperty):
    node_type: URIRef = bacnet["object-type"]


class BACnetURI(BacnetProperty):
    node_type: URIRef = bacnet["BACnetURI"]


class BACnetDevice(Node):
    node_type: URIRef = bacnet.BACnetDevice
    deviceId: BACnetDeviceId
    deviceName: BacnetDeviceName
    networkNumer: BACnetDescription
    address: BACnetAdress
    vendorId: BACnetVendorId
    uri: BACnetURI


class BACnetReference(ExternalReference):
    node_type: URIRef = ref.BacnetReference
    objectInstance: BACnetObjectInstance
    objectOf: BACnetObjectOf
    objectName: BacnetObjectName
    description: BACnetDescription
    objectType: BACnetObjectType
    uri: BACnetURI
