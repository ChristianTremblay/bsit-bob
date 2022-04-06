from typing import Any

from rdflib import URIRef

from bob import core

from ..core import (
    ExternalReference,
    Light,
    Medium,
    PropertyReference,
    p223,
    quantitykind,
    unit,
)
from .sensor import QuantifiableMeasuredProperty, Sensor, split_kwargs

__namespace__ = p223


class Movement(QuantifiableMeasuredProperty):
    hasExternalReference: ExternalReference


class MovementSensor(Sensor):
    measuresMedium: Medium = Light
    observesProperty: PropertyReference  # Movement

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        self.observesProperty = Movement(
            # isObservedBy=self,
            label=f"{self.label}.Movement",
            **_measure_kwargs,
        )


class OccupancySensor(MovementSensor):
    node_type: URIRef = p223.OccupancySensor
