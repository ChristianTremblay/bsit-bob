from __future__ import annotations

from typing import Any
from rdflib import URIRef

from ..core import s223, enum, quantitykind, unit, Medium

from .sensor import Sensor, QuantifiableMeasurement, split_kwargs

from ..property import (
    ObservableProperty,
    QuantifiableProperty,
    QuantifiableObservableProperty,
)

__namespace__ = s223


class HumidityMeasure(QuantifiableMeasurement):
    node_type: URIRef = s223.HumidityMeasure
    hasQuantityKind: URIRef = quantitykind.RelativeHumidity
    unit: URIRef = unit.PERCENT_RH
    ofSubstance: Medium


class HumiditySetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.RelativeHumidity
    unit: URIRef = unit.PERCENT_RH


class AirHumiditySensor(Sensor):
    """
    Air humidity sensor. Can model room sensor or duct sensor
    """

    node_type: URIRef = s223.HumiditySensor
    hasSubstance: URIRef = enum["Medium-Air"]
    hasQuantityKind: URIRef = quantitykind.RelativeHumidity
    observesProperty: HumidityMeasure
    measuresSubstance: URIRef = enum["Medium-Air"]

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        _measure = HumidityMeasure(
            ofSubstance=self.measuresSubstance,
            isObservedBy=self,
            label=f"{self.label}.Measure",
            **_measure_kwargs,
        )

        self.observesProperty = _measure
