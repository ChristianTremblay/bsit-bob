from .sensor import Sensor, QuantifiableMeasuredProperty, split_kwargs
from rdflib import URIRef
from typing import Any
from ..core import quantitykind, p223, unit, Medium, Light, PropertyReference

from bob import core

__namespace__ = p223


class Movement(QuantifiableMeasuredProperty):
    # ISSUE -- boolean or movement amount?
    unit: URIRef = unit.DEG_C


class MovementSensor(Sensor):
    measuresMedium: Medium = Light
    observesProperty: PropertyReference  # Movement

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        _measure = Movement(
            # isObservedBy=self,
            label=f"{self.label}.Movement",
            **_measure_kwargs,
        )
        self.observesProperty = _measure


class OccupancySensor(MovementSensor):
    node_type: URIRef = p223.OccupancySensor
