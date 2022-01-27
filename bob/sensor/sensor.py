from typing import List, Union
from rdflib import Graph, Namespace, URIRef, BNode, Literal, RDF, RDFS, XSD


from ..core import s223, quantitykind, unit
from ..core import Property, Connection, ConnectionPoint, Device, Segment, DomainSpace

from ..property import (
    ObservableProperty,
    QuantifiableProperty,
)


__namespace__ = s223


class Sensor(Device):
    """
    A Sensor produces an ObservableProperty (which may or may not be quantifiable. For example, it might just sense an alarm state, or occupancy. But usually it will produce a number, in which case it is associated with a QuantifiableObservableProperty).
    """

    node_type: URIRef = s223.Sensor
    # hasMeasurementLocation: Union[
    #    Device,
    #    Connection,
    #    Segment,
    #    ConnectionPoint,
    #    DomainSpace,
    # ]
    hasMeasuremantLocation: Connection
    hasMeasurementPrecision: QuantifiableProperty
    hasMeasurementUncertainty: QuantifiableProperty
    hasMaxRange: QuantifiableProperty
    hasMinRange: QuantifiableProperty
    observesProperty: ObservableProperty  # maxCount = 1


class DifferentialSensor(Sensor):
    "Differential sensor"
    node_type: URIRef = s223.DifferentialSensor
    # hasMeasurementLocation: # maxCount = 2, minCount=2


class VirtualSensor(Sensor):
    "Virtal Sensor"
    node_type: URIRef = s223.VirtualSensor
    # hasMeasurementLocation: # maxCount = 0
    hasFunctionInput: Property
