from .sensor import Sensor, QuantifiableMeasuredProperty, split_kwargs
from rdflib import URIRef
from typing import Any
from ..core import quantitykind, p223, unit, Medium, Air, Water, PropertyReference

from ..property import QuantifiableProperty, Setpoint

__namespace__ = p223


class Temperature(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.Temperature
    unit: URIRef
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor


class TemperatureSetpoint(Setpoint):
    hasQuantityKind: URIRef = quantitykind.Temperature
    unit: URIRef


class TemperatureSensor(Sensor):
    observesProperty: PropertyReference  # Temperature

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)
        if "unit" not in _measure_kwargs:
            raise ValueError(
                "You must provide units when defining a temperature sensor"
            )
        if "measuresMedium" not in _measure_kwargs:
            raise ValueError(
                "You must provide measuresMedium when defining a temperature sensor"
            )
        super().__init__(**_sensor_kwargs)
        self.observesProperty = Temperature(
            # isObservedBy=self,
            label=f"{self.label}.Temperature",
            **_measure_kwargs,
        )


class AirTemperatureSensor(TemperatureSensor):
    def __init__(self, **kwargs):
        super().__init__(measuresMedium=Air, unit=unit.DEG_C, **kwargs)


class WaterTemperatureSensor(TemperatureSensor):
    def __init__(self, **kwargs):
        super().__init__(measuresMedium=Water, unit=unit.DEG_C, **kwargs)
