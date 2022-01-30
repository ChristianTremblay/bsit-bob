from typing import List, Union
from rdflib import Graph, Namespace, URIRef, BNode, Literal, RDF, RDFS, XSD


from ..core import s223, enum, quantitykind, unit
from ..core import (
    Property,
    Connection,
    ConnectionPoint,
    Device,
    Segment,
    DomainSpace,
    Medium,
)

from ..property import (
    ObservableProperty,
    QuantifiableProperty,
    QuantifiableObservableProperty,
)


__namespace__ = s223


def split_kwargs(given_kwargs):
    # specific properties given to a sensor for creation
    # but that must be applied to the measure AKA
    # the observesProperty
    _prop = ["hasExternalReference", "hasValue"]
    measure_kwargs = {}
    _given_kwargs = given_kwargs.copy()  # need a copy
    for k, v in _given_kwargs.items():
        if k in _prop:
            measure_kwargs[k] = given_kwargs.pop(k)
    sensor_kwargs = given_kwargs
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
    A Sensor produces an ObservableProperty (which may or may not be quantifiable. For example, it might just sense an alarm state, or occupancy. But usually it will produce a number, in which case it is associated with a QuantifiableObservableProperty).
    """

    node_type: URIRef = s223.Sensor
    # ISSUE
    # How can I define that ?
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
    hasSubstance: Medium
    measuresSubstance: Medium
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


class Measurement(ObservableProperty):
    isObservedBy: Sensor
    ofSubstance: Medium
    # def __init__(self, **kwargs):
    #    if 'isObservedBy' in kwargs:
    #        _isobservedby = kwargs.pop("isObservedBy")
    #        self.isObservedBy = _isobservedby
    #    super().__init__(**kwargs)


class QuantifiableMeasurement(QuantifiableObservableProperty):
    isObservedBy: Sensor
    ofSubstance: Medium
    # hasQuantityKind: depends on sensor
    # unit: depends on quantityKind
    # def __init__(self, **kwargs):
    #    if 'isObservedBy' in kwargs:
    #        _isobservedby = kwargs.pop("isObservedBy")
    #        self.isObservedBy = _isobservedby
    #    super().__init__(**kwargs)
