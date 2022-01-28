from __future__ import annotations

from typing import Any
from rdflib import URIRef, util

from ..core import s223, enum, quantitykind, unit, Medium

from .sensor import Sensor, Measurement, QuantifiableMeasurement

from ..property import (
    ObservableProperty,
    QuantifiableProperty,
    QuantifiableObservableProperty,
)

__namespace__ = s223


class ParticulateCountMeasure(QuantifiableMeasurement):
    node_type: URIRef = s223.ParticulateMeasure
    hasQuantityKind: URIRef = quantitykind.NumberDensity
    ofSubstance: Medium
    hasUnit: URIRef = unit["NUM-PER-M3"]
    isObservedBy: Sensor
    ofSubstance: Medium


class ParticulateSensor(Sensor):
    node_type: URIRef = s223.ParticulateSensor
    hasSubstance: URIRef = enum.Medium_Air
    # hasQuantityKind: URIRef = quantitykind.MassDensity
    measuresSubstance: Medium
    observesProperty: ParticulateCountMeasure

    def __init__(self, **kwargs: Any) -> None:
        _hasExternalReference = None
        _hasValue = None
        if "extref" in kwargs:
            _hasExternalReference = kwargs.pop("extref")
        elif "value" in kwargs:
            _hasValue = kwargs.pop("value")
        super().__init__(**kwargs)
        _count = ParticulateCountMeasure(
            hasExternalReference=_hasExternalReference,
            hasValue=_hasValue,
            ofSubstance=self.measuresSubstance,
            isObservedBy=self,
        )

        self.observesProperty = _count


class UltraFineParticulateSensor(ParticulateSensor):
    "PM 1.0 Count"
    node_type = s223.UltraFineParticulateSensor
    measuresSubstance: URIRef = enum["Particulate-PM1.0"]

    def __init__(self, **kwargs):
        super().__init__(label="Ultra Fine Channel", comment="1.0 PM Channel", **kwargs)


class FineParticulateSensor(ParticulateSensor):
    "PM 2.5 Count"
    node_type = s223.FineParticulateSensor
    measuresSubstance: URIRef = enum["Particulate-PM2.5"]

    def __init__(self, **kwargs):
        super().__init__(label="Fine Channel", comment="2.5 PM Channel", **kwargs)


class CoarseParticulateSensor(ParticulateSensor):
    "PM 10 Count"
    node_type = s223.CoarseParticulateSensor
    measuresSubstance: URIRef = enum["Particulate-PM10"]

    def __init__(self, **kwargs):
        super().__init__(label="Coarse Channel", comment="10 PM Channel", **kwargs)
