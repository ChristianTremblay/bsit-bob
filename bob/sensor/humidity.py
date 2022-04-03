from __future__ import annotations

from typing import Any
from rdflib import URIRef

from ..core import PropertyReference, p223, enum, quantitykind, unit, Medium, Air

from .sensor import Sensor, QuantifiableMeasuredProperty, split_kwargs

from ..property import (
    ObservableProperty,
    QuantifiableProperty,
    QuantifiableObservableProperty,
)

__namespace__ = p223


class Humidity(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.RelativeHumidity
    unit: URIRef = unit.PERCENT_RH
    measuresMedium: Medium = Air


class HumiditySetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.RelativeHumidity
    unit: URIRef = unit.PERCENT_RH


class AirHumiditySensor(Sensor):
    """
    Air humidity sensor. Can model room sensor or duct sensor
    """

    measuresMedium: Medium = Air
    hasQuantityKind: URIRef = quantitykind.RelativeHumidity
    observesProperty: PropertyReference  # Humidity

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        self.observesProperty = Humidity(
            # isObservedBy=self,
            label=f"{self.label}.Measure",
            **_measure_kwargs,
        )
