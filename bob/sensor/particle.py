from __future__ import annotations

from typing import Any

from rdflib import URIRef, util

from ..core import (
    Air,
    Medium,
    PropertyReference,
    Substance,
    enum,
    p223,
    quantitykind,
    unit,
)
from ..enum import Particulate
from ..properties import ParticulateCount
from ..property import (
    ObservableProperty,
    QuantifiableObservableProperty,
    QuantifiableProperty,
    Setpoint,
)
from .sensor import Sensor, split_kwargs

_namespace = p223


class ParticulateSensor(Sensor):
    observesProperty: PropertyReference  # ParticulateCount

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observesProperty = ParticulateCount(
            label=f"{self.label}.ParticulateCount",  # needs more focus
            ofMedium=Air,
            **_property_kwargs,
        )


class UltraFineParticulateSensor(ParticulateSensor):
    "PM 1.0 Count"
    comment = "Ultra Fine Particulate Sensor"
    # measuresSubstance: Substance = PM1_0
    def __init__(self, **kwargs):
        super().__init__(ofSubstance=Particulate.PM1_0, **kwargs)


class FineParticulateSensor(ParticulateSensor):
    "PM 2.5 Count"
    comment = "Fine Particulate Sensor"
    # measuresSubstance: Substance = PM2_5
    def __init__(self, **kwargs):
        super().__init__(ofSubstance=Particulate.PM2_5, **kwargs)


class CoarseParticulateSensor(ParticulateSensor):
    "PM 10 Count"
    comment = "Coarse Particulate Sensor"
    # measuresSubstance: Substance = PM10_0
    def __init__(self, **kwargs):
        super().__init__(ofSubstance=Particulate.PM10_0, **kwargs)
