from .sensor import Sensor, QuantifiableMeasuredProperty, split_kwargs
from rdflib import URIRef
from typing import Any
from ..core import quantitykind, p223, unit, Medium, Air, Water, PropertyReference

from ..property import QuantifiableProperty

__namespace__ = p223


class Temperature(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.Temperature
    unit: URIRef = unit.DEG_C
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor


class TemperatureSetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.Temperature
    unit: URIRef = unit.DEG_C


class TemperatureSensor(Sensor):
    observesProperty: PropertyReference  # Temperature

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        if not self.measuresMedium:
            raise ValueError(
                "You must provide measuresMedium property for a temperature sensor either in config template or subclass defintion"
            )
        _measure = Temperature(
            measuresMedium=self.measuresMedium,
            # isObservedBy=self,
            label=f"{self.label}.Temperature",
            **_measure_kwargs,
        )
        self.observesProperty = _measure


class AirTemperatureSensor(TemperatureSensor):
    measuresMedium: Medium = Air


class WaterTemperatureSensor(TemperatureSensor):
    measuresMedium: Medium = Water
