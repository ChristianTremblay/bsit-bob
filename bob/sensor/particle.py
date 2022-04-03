from __future__ import annotations

from typing import Any
from rdflib import URIRef, util

from ..core import (
    PropertyReference,
    p223,
    enum,
    quantitykind,
    unit,
    Medium,
    Air,
    Substance,
)

from .sensor import Sensor, QuantifiableMeasuredProperty, split_kwargs

from ..property import (
    ObservableProperty,
    QuantifiableProperty,
    QuantifiableObservableProperty,
)

__namespace__ = p223

PM1_0 = Substance(node_iri=p223["Particulate-PM1.0"])
PM2_5 = Substance(node_iri=p223["Particulate-PM2.5"])
PM10_0 = Substance(node_iri=p223["Particulate-PM10.0"])


class ParticulateCount(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.NumberDensity
    unit: URIRef = unit["NUM-PER-M3"]
    measuresMedium: Medium
    measuresSubstance: Substance


class ParticulateSensor(Sensor):
    measuresMedium: Medium = Air
    observesProperty: PropertyReference  # ParticulateCount

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        self.observesProperty = ParticulateCount(
            measuresSubstance=self.measuresSubstance,
            # isObservedBy=self,
            label=f"{self.label}.ParticulateCount",  # needs more focus
            **_measure_kwargs,
        )


class UltraFineParticulateSensor(ParticulateSensor):
    "PM 1.0 Count"
    comment = "Ultra Fine Particulate Sensor"
    measuresSubstance: Substance = PM1_0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class FineParticulateSensor(ParticulateSensor):
    "PM 2.5 Count"
    comment = "Fine Particulate Sensor"
    measuresSubstance: Substance = PM2_5


class CoarseParticulateSensor(ParticulateSensor):
    "PM 10 Count"
    comment = "Coarse Particulate Sensor"
    measuresSubstance: Substance = PM10_0
