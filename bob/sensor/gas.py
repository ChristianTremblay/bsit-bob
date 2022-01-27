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

__namespace__ = s223, enum


class GasConcentrationMeasure(QuantifiableObservableProperty):
    node_type: URIRef = s223.HumidityMeasure
    hasQuantityKind: URIRef = quantitykind.Concentration
    # whew.... RelativeHumidity would have make sense here...
    # looks like something to talk with Steve Ray
    hasUnit: URIRef = unit.PPM


class GasConcentrationSetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.Concentration
    hasUnit: URIRef = unit.PPM


class GasConcentrationSensor(Sensor):
    node_type: URIRef = s223.GasConcentrationSensor
    # hasSubstance: URIRef = enum["Medium-Air"]
    hasQuantityKind: URIRef = quantitykind.RelativeHumidity
    observesProperty: GasConcentrationMeasure

    def __init__(self, **kwargs: Any) -> None:

        if "extref" in kwargs:
            _measure = GasConcentrationMeasure(
                hasExternalReference=kwargs.pop("extref")
            )
        elif "value" in kwargs:
            _measure = GasConcentrationMeasure(hasValue=kwargs.pop("value"))
        else:
            _measure = GasConcentrationMeasure()

        super().__init__(**kwargs)
        self.observesProperty = _measure


class CO2Sensor(GasConcentrationSensor):
    "Carbon Dioxide concentration sensor"
    hasSubstance: URIRef = enum["Substance-CO2"]


class COSensor(GasConcentrationSensor):
    "Carbon monoxide concentration sensor"
    hasSubstance: URIRef = enum["Substance-CO"]


class NO2Sensor(GasConcentrationSensor):
    "Diesel (NO2) concentration sensor"
    hasSubstance: URIRef = enum["Substance-NO2"]


class CH4Sensor(GasConcentrationSensor):
    "Natural gas sensor"
    hasSubstance: URIRef = enum["Substance-CH4"]
