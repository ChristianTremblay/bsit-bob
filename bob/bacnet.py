"""
This module contains just enough of the BACnet object model to help build
example models.  A complete description of BACnet objects and properties is
beyond the scope of this project.
"""
import logging
import re
from typing import Any, List

from rdflib import XSD, Literal, URIRef

from .core import Equipment, ExternalReference, Node, bind_namespace, INCLUDE_INVERSE
from .equipment.control.controller import Controller
from .externalreference.bacnet import BACnetExternalReference
from .multimethods import multimethod, new_class

# logging
_log = logging.getLogger(__name__)

# namespace
BACNET = bind_namespace("bacnet", "http://data.ashrae.org/bacnet/2020#")
_namespace = BACNET


class Device(Controller):
    _class_iri: URIRef = BACNET.Device
    _namespace = BACNET
    _device_object = Node
    _bacnet_objects = set()

class Object(Node):
    _attr_uriref = {
        "objectIdentifier": BACNET["object-identifier"],
        "objectName": BACNET["object-name"],
        "objectType": BACNET["object-type"],
        "description": BACNET["description"],
    }
    objectIdentifier: Literal
    objectName: Literal
    objectType: URIRef
    description: Literal
    ext_ref_args: list

    def create_external_reference_url(self, bacnet_device, propertyIdentifier="present-value"):
        _dev_instance = bacnet_device._device_object.objectIdentifier.split(',')[1]
        _label = f"dev_{_dev_instance}.{self.objectName}"
        _url = f"bacnet://{_dev_instance}/{self.objectIdentifier}/{propertyIdentifier}"
        self.ext_ref_args = [_label, _url]

    @property
    def present_value(self):
        "Creates the present_value on demand to be used as external reference for a property"
        _label, _url = self.ext_ref_args
        return BACnetExternalReference(_url, label=_label)

@multimethod
def contains_mm(device_: Device, object_: Object) -> None:
    """Device > Object"""
    _log.info(f"device {device_} contains object {object_}")
    if isinstance(object_, DeviceObject):
        device_._device_object = object_
    else:
        device_._bacnet_objects.add(object_)
        object_.create_external_reference_url(device_)
    device_._data_graph.add((device_._node_iri, BACNET.hasObject, object_._node_iri))
    if INCLUDE_INVERSE:
        device_._data_graph.add(
            (object_._node_iri, BACNET.isObjectOf, device_._node_iri)
        )


@multimethod
def contains_mm(device_: Device, object_list: List[Object]) -> None:
    """Device > Object"""
    _log.info(f"device {device_} contains object list {object_list}")

    for object_ in object_list:
        contains_mm(device_, object_)


class DeviceObject(Object):
    objectType: URIRef = BACNET["ObjectType.device"]
    _attr_uriref = {
        "systemStatus": BACNET["system-status"],
        "vendorName": BACNET["vendor-name"],
        "vendorIdentifier": BACNET["vendor-identifier"],
    }
    systemStatus: URIRef  # one of bacnet:DeviceStatus
    vendorName: Literal
    vendorIdentifier: XSD.nonNegativeInteger


class AnalogInputObject(Object):
    objectType: URIRef = BACNET["ObjectType.analog-input"]


class AnalogOutputObject(Object):
    objectType: URIRef = BACNET["ObjectType.analog-output"]


class AnalogValueObject(Object):
    objectType: URIRef = BACNET["ObjectType.analog-value"]


class BinaryInputObject(Object):
    objectType: URIRef = BACNET["ObjectType.binary-input"]


class BinaryOutputObject(Object):
    objectType: URIRef = BACNET["ObjectType.binary-output"]


class BinaryValueObject(Object):
    objectType: URIRef = BACNET["ObjectType.binary-value"]


class CalendarObject(Object):
    objectType: URIRef = BACNET["ObjectType.calendar"]


class ScheduleObject(Object):
    objectType: URIRef = BACNET["ObjectType.schedule"]
