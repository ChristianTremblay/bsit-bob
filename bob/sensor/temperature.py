from typing import Any

from rdflib import URIRef

from ..core import (
    Air,
    Medium,
    PropertyReference,
    Water,
    bob,
    p223,
    quantitykind,
    s223,
    unit,
)
from ..properties import Temperature
from ..property import QuantifiableProperty, Setpoint
from .sensor import Sensor, split_kwargs

_namespace = bob


class TemperatureSetpoint(Setpoint):
    _class_iri = s223.Setpoint
    hasQuantityKind: URIRef = quantitykind.Temperature
    unit: URIRef


class TemperatureSensor(Sensor):
    _class_iri = s223.Sensor
    observesProperty: PropertyReference  # Temperature
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "unit" not in _property_kwargs:
            raise ValueError(
                "You must provide units when defining a temperature sensor"
            )
        if "ofMedium" not in _property_kwargs:
            raise ValueError(
                "You must provide ofMedium when defining a temperature sensor"
            )

        super().__init__(**_sensor_kwargs)

        self.observesProperty = Temperature(
            # isObservedBy=self,
            label=f"{self.label}.Temperature",
            **_property_kwargs,
        )


class AirTemperatureSensor(TemperatureSensor):
    _class_iri = s223.Sensor

    def __init__(self, **kwargs):
        super().__init__(ofMedium=Air, **kwargs)


class WaterTemperatureSensor(TemperatureSensor):
    _class_iri = s223.Sensor

    def __init__(self, **kwargs):
        super().__init__(ofMedium=Water, **kwargs)
