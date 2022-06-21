from __future__ import annotations

from typing import Any, List, Union

from rdflib import RDF, RDFS, XSD, BNode, Graph, Literal, Namespace, URIRef

from ..core import (
    INCLUDE_INVERSE,
    Connection,
    ConnectionPoint,
    Device,
    DomainSpace,
    ExternalReference,
    Medium,
    Node,
    Property,
    PropertyReference,
    Segment,
    Substance,
    BOB,
    logging,
    P223,
    QUANTITYKIND,
    S223,
    UNIT,
)
from ..multimethods import multimethod
from ..property import (
    ObservableProperty,
    QuantifiableObservableProperty,
    QuantifiableProperty,
)

_namespace = S223


def split_kwargs(given_kwargs):
    # specific properties given to a sensor for creation
    # but that must be applied to the observed property, see
    # sorted(QuantifiableObservableProperty._attr_uriref.keys())
    property_attrs = [
        "hasExternalReference",
        "hasQuantityKind",
        "hasSetpoint",
        "hasValue",
        "ofMedium",
        "ofSubstance",
        "unit",
    ]
    property_kwargs = {}
    sensor_kwargs = {}
    for k, v in given_kwargs.items():
        if v is None:
            continue
        if k in property_attrs:
            property_kwargs[k] = v
        else:
            sensor_kwargs[k] = v

    return (sensor_kwargs, property_kwargs)


def define_sensors(config):
    if not config:
        return []
    sensors = []
    for sensor_label_and_class, sensor_data in config["sensors"].items():
        _label, _cls = sensor_label_and_class
        try:
            if issubclass(_cls, Sensor):
                _cls = _cls
        except:
            raise TypeError("Please provide class for sensor")

        sensors.append(_cls(label=_label, **sensor_data))

    return sensors


class Sensor(Device):
    """
    A Sensor provides a value for an ObservableProperty which may or may not
    be quantifiable. For example, it might just sense an alarm state, or
    occupancy. But usually it will produce a number, in which case it is
    associated with a QuantifiableObservableProperty.

    A sensor can have only one measurement (observesProperty)
    """

    _class_iri: URIRef = S223.Sensor
    # ISSUE
    # How can I define that ?
    # hasMeasurementLocation: Union[
    #    Device,
    #    Connection,
    #    Segment,
    #    ConnectionPoint,
    #    DomainSpace
    # ]
    hasMeasurementLocation: Node
    hasMeasurementPrecision: QuantifiableProperty
    hasMeasurementUncertainty: QuantifiableProperty
    hasMaxRange: QuantifiableProperty
    hasMinRange: QuantifiableProperty
    # measuresMedium: Medium
    # measuresSubstance: Substance  # When substance measured different than medium (ex. Gas)
    observesProperty: PropertyReference  ### restrict to MeasuredProperty

    def __gt__(self, other: Node) -> Any:
        """contains multimethod"""
        contains_mm(self, other)
        return self

    def __lt__(self, other: Node) -> Any:
        """contains multimethod"""
        contains_mm(other, self)
        return self

    def __matmul__(self, other: Node) -> Any:
        """contains multimethod"""
        contains_mm(self, other)
        return self


@multimethod
def contains_mm(parent_device: Device, child_device: Sensor) -> None:
    """Device > Device"""
    logging.info(f"device {parent_device} contains device {child_device}")
    parent_device._data_graph.add(
        (parent_device._node_iri, S223.contains, child_device._node_iri)
    )
    if INCLUDE_INVERSE:
        parent_device._data_graph.add(
            (child_device._node_iri, S223.isContainedIn, parent_device._node_iri)
        )


@multimethod
def contains_mm(parent_device: Sensor, child_device: ExternalReference) -> None:
    """Device > Device"""
    logging.info(f"device {parent_device} contains device {child_device}")
    parent_device._data_graph.add(
        (
            parent_device.observesProperty._node_iri,
            S223.hasExternalReference,
            child_device._node_iri,
        )
    )
    if INCLUDE_INVERSE:
        parent_device._data_graph.add(
            (
                child_device._node_iri,
                S223.isExternalReferenceOf,
                parent_device.observesProperty._node_iri,
            )
        )


class DifferentialSensor(Sensor):
    "Differential sensor"
    _class_iri: URIRef = S223.DifferentialSensor
    hasMeasurementLocationHigh: Node  # I don't know how to type a list of 2 nodes...
    hasMeasurementLocationLow: Node


class VirtualSensor(Sensor):
    "Virtal Sensor"
    _class_iri: URIRef = S223.VirtualSensor
    # hasMeasurementLocation: # maxCount = 0
    hasFunctionInput: Property


# class MeasuredProperty(ObservableProperty):
#    _class_iri: URIRef = None
#    isObservedBy: Sensor


# class QuantifiableMeasuredProperty(QuantifiableObservableProperty, MeasuredProperty):
#    _class_iri: URIRef = None
# hasQuantityKind inherited from QuantifiableProperty
# isObservedBy inherited from MeasuredProperty
