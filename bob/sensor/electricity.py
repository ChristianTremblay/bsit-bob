from typing import Any

from rdflib import URIRef

from ..core import (
    Air,
    Electricity,
    Medium,
    Node,
    PropertyReference,
    Water,
    bob,
    p223,
    quantitykind,
    s223,
    unit,
)
from ..properties import Amps, OnOffStatus, Volts
from ..property import ObservableProperty, QuantifiableProperty
from .sensor import Sensor, split_kwargs

_namespace = bob


class VoltageSensor(Sensor):
    _class_iri = s223.Sensor
    observesProperty: PropertyReference  # Temperature
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "ofMedium" not in _property_kwargs:
            raise ValueError("You must provide ofMedium when defining a voltage sensor")

        super().__init__(**_sensor_kwargs)

        self.observesProperty = Volts(
            # isObservedBy=self,
            label=f"{self.label}.Voltage",
            **_property_kwargs,
        )


class CurrentAnalogSensor(Sensor):
    _class_iri = s223.Sensor
    observesProperty: PropertyReference  # Temperature
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "ofMedium" not in _property_kwargs:
            raise ValueError("You must provide ofMedium when defining a current sensor")

        super().__init__(**_sensor_kwargs)

        self.observesProperty = Amps(
            # isObservedBy=self,
            label=f"{self.label}.Amps",
            **_property_kwargs,
        )


class CurrentBinarySensor(Sensor):
    _class_iri = s223.Sensor
    observesProperty: PropertyReference  # Electrical Current
    hasMeasurementLocation: Node

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observesProperty = OnOffStatus(
            # isObservedBy=self,
            label=f"{self.label}.CurrentBinarySensor",
            **_property_kwargs,
        )
