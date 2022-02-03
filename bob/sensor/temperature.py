from .sensor import Sensor, Measurement, QuantifiableMeasurement, split_kwargs
from rdflib import URIRef
from typing import Any
from ..core import quantitykind, s223, unit, enum, Medium

from ..property import QuantifiableObservableProperty, QuantifiableProperty

from bob import core

__namespace__ = s223


class TemperatureMeasure(QuantifiableMeasurement):
    node_type: URIRef = s223.TemperatureMeasure
    hasQuantityKind: URIRef = quantitykind.Temperature
    unit: URIRef = unit.DEG_C
    # isObservedBy: Sensor
    ofSubstance: Medium


class TemperatureSetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.Temperature
    unit: URIRef = unit.DEG_C


class TemperatureSensor(Sensor):
    node_type: URIRef = s223.TemperatureSensor
    observesProperty: TemperatureMeasure

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        if not self.measuresSubstance:
            raise ValueError(
                "You must provide measuresSubstance property for a temperature sensor either in config template or subclass defintion"
            )
        _measure = TemperatureMeasure(
            ofSubstance=self.measuresSubstance,
            # isObservedBy=self,
            label=f"{self.label}.Measure",
            **_measure_kwargs,
        )
        self.observesProperty = _measure


class AirTemperatureSensor(TemperatureSensor):
    hasSubstance: URIRef = enum["Medium-Air"]
    measuresSubstance: URIRef = enum["Medium-Air"]


class WaterTemperatureSensor(TemperatureSensor):
    hasSubstance: URIRef = enum["Medium-Water"]
    measuresSubstance: URIRef = enum["Medium-Water"]
