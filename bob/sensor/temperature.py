from .sensor import Sensor, Measurement, QuantifiableMeasurement
from rdflib import URIRef
from typing import Any
from ..core import quantitykind, s223, unit, enum, Medium

from ..property import QuantifiableObservableProperty, QuantifiableProperty


__namespace__ = s223


class TemperatureMeasure(QuantifiableMeasurement):
    node_type: URIRef = s223.TemperatureMeasure
    hasQuantityKind: URIRef = quantitykind.Temperature
    unit: URIRef = unit.DEG_C
    isObservedBy: Sensor
    ofSubstance: Medium


class TemperatureSetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.Temperature
    unit: URIRef = unit.DEG_C


class TemperatureSensor(Sensor):
    node_type: URIRef = s223.TemperatureSensor
    observesProperty: TemperatureMeasure

    def __init__(self, **kwargs: Any) -> None:
        _refs = None
        _val = None
        if "extref" in kwargs:
            _refs = kwargs.pop("extref")

        elif "value" in kwargs:
            _val = kwargs.pop("value")

        super().__init__(**kwargs)
        _measure = TemperatureMeasure(
            hasExternalReference=_refs,
            hasValue=_val,
            ofSubstance=self.measuresSubstance,
            isObservedBy=self,
            label=f"{self.label}.Measure",
        )
        self.observesProperty = _measure


class AirTemperatureSensor(TemperatureSensor):
    hasSubstance: URIRef = enum["Medium-Air"]
    measuresSubstance: URIRef = enum["Medium-Air"]


class WaterTemperatureSensor(TemperatureSensor):
    hasSubstance: URIRef = enum["Medium-Water"]
    measuresSubstance: URIRef = enum["Medium-Water"]
