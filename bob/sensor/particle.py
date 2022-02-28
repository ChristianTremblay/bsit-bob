from __future__ import annotations

from typing import Any
from rdflib import URIRef, util

from ..core import s223, enum, quantitykind, unit, Medium

from .sensor import Sensor, Measurement, QuantifiableMeasurement, split_kwargs

from ..property import (
    ObservableProperty,
    QuantifiableProperty,
    QuantifiableObservableProperty,
)

__namespace__ = s223


class ParticulateCountMeasure(QuantifiableMeasurement):
    node_type: URIRef = s223.Measure
    hasQuantityKind: URIRef = quantitykind.NumberDensity
    unit: URIRef = unit["NUM-PER-M3"]


class ParticulateSensor(Sensor):
    node_type: URIRef = s223.ParticulateSensor
    hasMedium: URIRef = s223["Medium-Air"]
    measuresSubstance: Medium
    observesProperty: ParticulateCountMeasure

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        _count = ParticulateCountMeasure(
            ofSubstance=self.measuresSubstance,
            # isObservedBy=self,
            label=f"{self.label}.Measure",
            **_measure_kwargs,
        )

        self.observesProperty = _count


class UltraFineParticulateSensor(ParticulateSensor):
    "PM 1.0 Count"
    node_type = s223.ParticulateSensor
    comment = "Ultra Fine Particulate Sensor"
    measuresSubstance: URIRef = s223["Particulate-PM1.0"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class FineParticulateSensor(ParticulateSensor):
    "PM 2.5 Count"
    node_type = s223.ParticulateSensor
    comment = "Fine Particulate Sensor"
    measuresSubstance: URIRef = s223["Particulate-PM2.5"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CoarseParticulateSensor(ParticulateSensor):
    "PM 10 Count"
    node_type = s223.ParticulateSensor
    comment = "Coarse Particulate Sensor"
    measuresSubstance: URIRef = s223["Particulate-PM10.0"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
