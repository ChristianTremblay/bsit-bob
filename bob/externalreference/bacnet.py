import logging
import re
from typing import Any

from rdflib import Literal, URIRef, XSD

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


class BACnetDevice(Node):
    _class_iri: URIRef = bacnet.BACnetDevice
    deviceId: XSD.integer
    deviceName: Literal
    networkNumber: XSD.integer
    address: XSD.integer
    vendorId: XSD.integer


class BACnetReference(ExternalReference):
    _class_iri: URIRef = ref.BACnetReference
    objectInstance: XSD.integer
    objectOf: BACnetDevice
    objectName: Literal
    description: Literal
    objectType: Literal
    uri: URIRef

    def __init__(self, arg: str = "", **kwargs) -> None:
        logging.debug("BACnetReference.__init__ %r %r", arg, kwargs)

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

            # future work
            # if "objectIdentifier" in kwargs:
            #     raise ValueError("initialization conflict: objectIdentifier")
            # kwargs["objectIdentifier"] = f"{object_type},{object_instance}"

        super().__init__(**kwargs)
