from __future__ import annotations

from typing import Any
from rdflib import URIRef

from ..core import s223, enum, quantitykind, unit

from .sensor import Sensor

from ..property import (
    ObservableProperty,
    QuantifiableProperty,
    QuantifiableObservableProperty,
)

__namespace__ = s223


class ParticulateMeasure(QuantifiableObservableProperty):
    node_type: URIRef = s223.ParticulateMeasure
    hasQuantityKind: URIRef = quantitykind.MassDensity
    ofSubstance: URIRef = enum["Substance-Particulate"]
    hasUnit: URIRef = unit["MicroGM-PER-M3"]


class ParticulatCount(QuantifiableObservableProperty):
    node_type: URIRef = s223.ParticulateCount
    hasQuantityKind: URIRef = quantitykind.Concentration
    ofSubstance: URIRef = enum["Substance-Particulate"]
    hasUnit: URIRef = unit["NUM-PER-M3"]


class ParticulateSensor(Sensor):
    node_type: URIRef = s223.ParticulateSensor
    # hasSubstance: URIRef = enum.Medium_Air
    # hasQuantityKind: URIRef = quantitykind.MassDensity
    observesProperty: ParticulateMeasure
    particleCount: ParticulatCount

    def __init__(self, **kwargs: Any) -> None:

        if "extref" in kwargs:
            _count = ParticulatCount(hasExternalReference=kwargs.pop("extref"))
        elif "value" in kwargs:
            _count = ParticulatCount(hasValue=kwargs.pop("value"))
        else:
            _count = ParticulatCount()

        super().__init__(**kwargs)
        self.observesProperty = ParticulateMeasure()
        self.particleCount = _count


class UltraFineParticulateSensor(ParticulateSensor):
    "PM 1.0 Count"
    hasSubstance: URIRef = enum["Particulate-PM1.0"]

    def __init__(self, extref=None):
        super().__init__(
            label="Ultra Fine Channel", comment="1.0 PM Channel", extref=extref
        )


class FineParticulateSensor(ParticulateSensor):
    "PM 2.5 Count"
    hasSubstance: URIRef = enum["Particulate-PM2.5"]

    def __init__(self, extref=None):
        super().__init__(label="Fine Channel", comment="2.5 PM Channel", extref=extref)


class CoarseParticulateSensor(ParticulateSensor):
    "PM 10 Count"
    hasSubstance: URIRef = enum["Particulate-PM10"]

    def __init__(self, extref=None):
        super().__init__(label="Coarse Channel", comment="10 PM Channel", extref=extref)
