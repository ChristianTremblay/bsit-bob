import logging
import re
from typing import Any

from rdflib import Literal, URIRef

from ..core import (
    Device,
    EnumerationKind,
    ExternalReference,
    Graph,
    Node,
    bacnet,
    p223,
    ref,
    schema_graph,
)

_namespace = p223

url_pattern = re.compile("^bacnet:[/][/]([0-9]+)[/]([A-Za-z0-9-]+),([1-9][0-9]*)$")


class BACnetProperty(Node):
    _class_iri: URIRef = bacnet.Property
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
    _class_iri: URIRef = bacnet["device-identifier"]


class BACnetDeviceName(BACnetProperty):
    _class_iri: URIRef = bacnet["device-name"]


class BACnetNetworkNumber(BACnetProperty):
    _class_iri: URIRef = bacnet["network-number"]


class BACnetAddress(BACnetProperty):
    _class_iri: URIRef = bacnet["address"]


class BACnetVendorId(BACnetProperty):
    _class_iri: URIRef = bacnet["vendor-id"]


class BACnetObjectInstance(BACnetProperty):
    _class_iri: URIRef = bacnet["object-instance"]


class BACnetObjectOf(BACnetProperty):
    _class_iri: URIRef = bacnet["BACnetDevice"]


class BACnetObjectName(BACnetProperty):
    _class_iri: URIRef = bacnet["object-name"]


class BACnetDescription(BACnetProperty):
    _class_iri: URIRef = bacnet["description"]


class BACnetObjectType(BACnetProperty):
    _class_iri: URIRef = bacnet["object-type"]


class BACnetURI(BACnetProperty):
    _class_iri: URIRef = bacnet["BACnetURI"]


class BACnetDevice(Node):
    _class_iri: URIRef = bacnet.BACnetDevice
    deviceId: BACnetDeviceId
    deviceName: BACnetDeviceName
    networkNumber: BACnetNetworkNumber
    address: BACnetAddress
    vendorId: BACnetVendorId
    uri: BACnetURI


class BACnetReference(ExternalReference):
    _class_iri: URIRef = ref.BACnetReference
    objectInstance: BACnetObjectInstance
    objectOf: BACnetObjectOf
    objectName: BACnetObjectName
    description: BACnetDescription
    objectType: BACnetObjectType
    uri: BACnetURI

    def __init__(self, arg: str = "", **kwargs) -> None:
        logging.debug("__init__ %r %r", arg, kwargs)

        if arg:
            url_match = url_pattern.match(arg)
            if not url_match:
                raise ValueError("not a BACnet URL")
            device, object_type, object_instance = url_match.groups()

            if "objectType" in kwargs:
                raise ValueError("initialization conflict: objectType")
            kwargs["objectType"] = object_type

            if "objectInstance" in kwargs:
                raise ValueError("initialization conflict: objectInstance")
            kwargs["objectInstance"] = int(object_instance)

        super().__init__(**kwargs)
