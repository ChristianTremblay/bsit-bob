from __future__ import annotations

from typing import Any
from rdflib import URIRef

from ..core import s223, enum, quantitykind, unit

from .sensor import Sensor, QuantifiableMeasurement

from ..property import (
    ObservableProperty,
    QuantifiableProperty,
    QuantifiableObservableProperty,
)

__namespace__ = s223

class GasConcentrationMeasure(QuantifiableMeasurement):
    node_type: URIRef = s223.HumidityMeasure
    hasQuantityKind: URIRef = quantitykind.Concentration
    # whew.... RelativeHumidity would have make sense here...
    # looks like something to talk with Steve Ray
    unit: URIRef = unit.PPM
    #measuresSubstance: URIRef
    isObservedBy: Sensor

class GasConcentrationSetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.Concentration
    unit: URIRef = unit.PPM


class GasConcentrationSensor(Sensor):
    node_type: URIRef = s223.GasConcentrationSensor
    # hasSubstance: URIRef = enum["Medium-Air"]
    hasQuantityKind: URIRef = quantitykind.Concentration
    hasSubstance: URIRef = enum['Medium-Air']
    observesProperty: GasConcentrationMeasure

    def __init__(self, **kwargs: Any) -> None:

        _refs = None
        _val = None
        if "extref" in kwargs:
            _refs = kwargs.pop("extref")
            
        elif "value" in kwargs:
            _val = kwargs.pop("value")

        super().__init__(**kwargs)
        _measure = GasConcentrationMeasure(hasValue=kwargs.pop("value"), hasValue=_val, ofSubstance=self.measuresSubstance,  isObservedBy=self)
        self.observesProperty = _measure


class CO2Sensor(GasConcentrationSensor):
    "Carbon Dioxide concentration sensor"
    measuresSubstance: URIRef = enum["Substance-CO2"]


class COSensor(GasConcentrationSensor):
    "Carbon monoxide concentration sensor"
    measuresSubstance: URIRef = enum["Substance-CO"]


class NO2Sensor(GasConcentrationSensor):
    "Diesel (NO2) concentration sensor"
    measuresSubstance: URIRef = enum["Substance-NO2"]


class CH4Sensor(GasConcentrationSensor):
    "Natural gas sensor"
    measuresSubstance: URIRef = enum["Substance-CH4"]
