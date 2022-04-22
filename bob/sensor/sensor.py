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
    logging,
    p223,
    quantitykind,
    s223,
    unit,
)
from ..multimethods import multimethod
from ..property import (
    ObservableProperty,
    QuantifiableObservableProperty,
    QuantifiableProperty,
)

_namespace = s223


def split_kwargs(given_kwargs):
    # specific properties given to a sensor for creation
    # but that must be applied to the measure AKA
    # the observesProperty
    _prop = [
        "hasExternalReference",
        "hasValue",
        "unit",
        "hasQuantityKind",
        "measuresMedium",
    ]
    measure_kwargs = {}
    sensor_kwargs = {}
    _given_kwargs = given_kwargs.copy()  # need a copy
    for k, v in _given_kwargs.items():
        if k in _prop:
            if v is not None:
                measure_kwargs[k] = given_kwargs.pop(k)
        else:
            if v is not None:
                sensor_kwargs[k] = given_kwargs.pop(k)
    return (sensor_kwargs, measure_kwargs)


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

    node_type: URIRef = s223.Sensor
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
    measuresMedium: Medium
    measuresSubstance: Substance  # When substance measured different than medium (ex. Gas)
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
        (parent_device.node, s223.contains, child_device.node)
    )
    if INCLUDE_INVERSE:
        parent_device._data_graph.add(
            (child_device.node, s223.isContainedIn, parent_device.node)
        )


@multimethod
def contains_mm(parent_device: Sensor, child_device: ExternalReference) -> None:
    """Device > Device"""
    logging.info(f"device {parent_device} contains device {child_device}")
    parent_device._data_graph.add(
        (
            parent_device.observesProperty.node,
            s223.hasExternalReference,
            child_device.node,
        )
    )
    if INCLUDE_INVERSE:
        parent_device._data_graph.add(
            (
                child_device.node,
                s223.isExternalReferenceOf,
                parent_device.observesProperty.node,
            )
        )


class DifferentialSensor(Sensor):
    "Differential sensor"
    node_type: URIRef = s223.DifferentialSensor
    # hasMeasurementLocation: # maxCount = 2, minCount=2


class VirtualSensor(Sensor):
    "Virtal Sensor"
    node_type: URIRef = s223.VirtualSensor
    # hasMeasurementLocation: # maxCount = 0
    hasFunctionInput: Property


# class MeasuredProperty(ObservableProperty):
#    node_type: URIRef = None
#    isObservedBy: Sensor


# class QuantifiableMeasuredProperty(QuantifiableObservableProperty, MeasuredProperty):
#    node_type: URIRef = None
# hasQuantityKind inherited from QuantifiableProperty
# isObservedBy inherited from MeasuredProperty
