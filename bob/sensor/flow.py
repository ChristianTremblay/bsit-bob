from .sensor import Sensor, Measurement, QuantifiableMeasurement, split_kwargs
from rdflib import URIRef
from typing import Any
from ..core import quantitykind, s223, p223, unit, enum, Medium

from ..property import QuantifiableObservableProperty, QuantifiableProperty

from bob import core

__namespace__ = p223


class FlowMeasure(QuantifiableMeasurement):
    node_type: URIRef = p223.Measure
    hasQuantityKind: URIRef = quantitykind.VolumeFlowRate
    unit: URIRef = unit["FT3-PER-MIN"]
    # isObservedBy: Sensor
    ofSubstance: Medium


class FlowSetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.Temperature
    unit: URIRef = unit.DEG_C


class FlowSensor(Sensor):
    node_type: URIRef = p223.FlowSensor
    observesProperty: FlowMeasure

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        if not self.measuresSubstance:
            raise ValueError(
                "You must provide measuresSubstance property for a temperature sensor either in config template or subclass defintion"
            )
        _measure = FlowMeasure(
            ofSubstance=self.measuresSubstance,
            # isObservedBy=self,
            label=f"{self.label}.Measure",
            **_measure_kwargs,
        )
        self.observesProperty = _measure


class AirFlowSensor(FlowSensor):
    hasMedium: URIRef = enum["Medium-Air"]
    measuresSubstance: URIRef = enum["Medium-Air"]
    unit: URIRef = unit["FT3-PER-MIN"]


class WaterFlowSensor(FlowSensor):
    hasMedium: URIRef = enum["Medium-Water"]
    measuresSubstance: URIRef = enum["Medium-Water"]
    unit: URIRef = unit["GAL_UK-PER-MIN"]
