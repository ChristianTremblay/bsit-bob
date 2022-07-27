import logging
import re
from typing import Any

from rdflib import XSD, Literal, URIRef

from ..core import (
    bind_namespace,
    Device,
    ExternalReference,
    Node,
)
from ..devices.control.controller import Controller


BACNET = bind_namespace("bacnet", "http://data.ashrae.org/bacnet/2020#")

url_pattern = re.compile(
    "^bacnet:[/][/]([0-9]+)[/]([A-Za-z0-9-]+),([1-9][0-9]*)(?:[/]([A-Za-z0-9-]+)+(?:[/]([1-9][0-9]*)))?$"
)


class BACnetDevice(Node):
    _class_iri: URIRef = BACNET.Device
    _namespace = BACNET
    deviceId: XSD.integer
    deviceName: Literal
    networkNumber: XSD.integer
    address: XSD.integer
    vendorId: XSD.integer
    isNetworkProfileOf: Controller


class BACnetReference(ExternalReference):
    _class_iri: URIRef = BACNET.DeviceObjectPropertyReference
    _namespace = BACNET
    _attr_uriref = {
        "objectName": BACNET["object-name"],
        "objectInstance": BACNET["object-instance"],
        "objectType": BACNET["object-type"],
        "propertyIdentifier": BACNET["property-identifier"],
        "propertyArrayIndex": BACNET["property-array-index"],
    }
    objectInstance: XSD.integer
    objectOf: BACnetDevice
    objectName: Literal
    description: Literal
    objectType: URIRef
    propertyIdentifier: URIRef
    propertyArrayIndex: XSD.nonNegativeInteger

    def __init__(self, arg: str = "", **kwargs) -> None:
        logging.debug("BACnetReference.__init__ %r %r", arg, kwargs)

        if arg:
            url_match = url_pattern.match(arg)
            if not url_match:
                raise ValueError("not a BACnet URL")
            (
                device,
                object_type,
                object_instance,
                property_identifier,
                property_array_index,
            ) = url_match.groups()

            if "objectType" in kwargs:
                raise ValueError("initialization conflict: objectType")
            kwargs["objectType"] = BACNET["ObjectType-" + object_type]

            if "objectInstance" in kwargs:
                raise ValueError("initialization conflict: objectInstance")
            kwargs["objectInstance"] = int(object_instance)

            # future work
            # if "objectIdentifier" in kwargs:
            #     raise ValueError("initialization conflict: objectIdentifier")
            # kwargs["objectIdentifier"] = f"{object_type},{object_instance}"

            if "propertyIdentifier" in kwargs:
                raise ValueError("initialization conflict: propertyIdentifier")
            if property_identifier:
                kwargs["propertyIdentifier"] = BACNET[
                    "PropertyIdentifier-" + property_identifier
                ]
            else:
                kwargs["propertyIdentifier"] = BACNET[
                    "PropertyIdentifier-present-value"
                ]

            if "propertyArrayIndex" in kwargs:
                raise ValueError("initialization conflict: propertyArrayIndex")
            if property_array_index:
                kwargs["propertyArrayIndex"] = int(property_array_index)

        if object_type := kwargs.get("objectType", None):
            if not isinstance(object_type, URIRef):
                kwargs["objectType"] = BACNET["ObjectType-" + object_type]

        super().__init__(**kwargs)
