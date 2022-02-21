from .sensor import Sensor, Measurement, QuantifiableMeasurement, split_kwargs
from rdflib import URIRef
from typing import Any
from ..core import quantitykind, s223, p223, unit, enum, Medium

from ..property import QuantifiableObservableProperty, QuantifiableProperty

from bob import core

__namespace__ = p223


class MovementMeasure(Measurement):
    node_type: URIRef = p223.Measure
    unit: URIRef = unit.DEG_C
    # isObservedBy: Sensor
    ofSubstance: Medium


class MovementSensor(Sensor):
    node_type: URIRef = p223.MovementSensor
    observesProperty: MovementMeasure
    measuresSubstance: URIRef = enum["Medium-Light"]

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        _measure = MovementMeasure(
            ofSubstance=self.measuresSubstance,
            # isObservedBy=self,
            label=f"{self.label}.Measure",
            **_measure_kwargs,
        )
        self.observesProperty = _measure
