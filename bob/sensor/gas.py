from __future__ import annotations

from typing import Any
from rdflib import URIRef

from ..core import s223, enum, quantitykind, unit, Value, Medium

from .sensor import Sensor, QuantifiableObservableProperty, split_kwargs

from ..property import (
    QuantifiableProperty,
)

__namespace__ = s223

# TODO :
# try to create an exmaple for the sensors found here
# Sal will like :0)
# And those are from Quebec
# http://operadetectors.com/category/gas-monitors-1.aspx


class GasConcentrationMeasure(QuantifiableObservableProperty):
    """
    Doc
    """

    node_type: URIRef = s223.Measure

    hasQuantityKind: URIRef = quantitykind.DimensionlessRatio
    ofSubstance: Medium
    unit: URIRef = unit.PPM
    # measuresSubstance: URIRef
    # isObservedBy: Sensor


class GasConcentrationSetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.DimensionlessRatio
    unit: URIRef = unit.PPM


class GasConcentrationSensor(Sensor):
    node_type: URIRef = s223.ConcentrationSensor
    hasQuantityKind: URIRef = quantitykind.DimensionlessRatio
    hasMedium: URIRef = enum["Medium-Air"]
    observesProperty: GasConcentrationMeasure

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)
        super().__init__(**_sensor_kwargs)
        _measure = GasConcentrationMeasure(
            ofSubstance=self.measuresSubstance,
            # isObservedBy=self,
            label=f"{self.label}.Measure",
            **_measure_kwargs,
        )

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
