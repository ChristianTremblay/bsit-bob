from .sensor import Sensor, QuantifiableMeasuredProperty, split_kwargs
from rdflib import URIRef
from typing import Any
from ..core import (
    quantitykind,
    s223,
    p223,
    unit,
    enum,
    Medium,
    Air,
    Water,
    PropertyReference,
)

from ..property import QuantifiableProperty

from bob import core

__namespace__ = p223


class Flow(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.VolumeFlowRate
    unit: URIRef = unit["FT3-PER-MIN"]
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor


class FlowSetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.VolumeFlowRate
    unit: URIRef = unit["FT3-PER-MIN"]  # match units of Flow?


class FlowSensor(Sensor):
    node_type: URIRef = p223.FlowSensor
    observesProperty: PropertyReference  # Flow

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        if not self.measuresMedium:
            raise ValueError(
                "You must provide measuresMedium property for a temperature sensor either in config template or subclass defintion"
            )
        self.measure = Flow(
            measuresMedium=self.measuresMedium,
            # isObservedBy=self,
            label=f"{self.label}.Flow",
            **_measure_kwargs,
        )
        self.observesProperty = self.measure


class AirFlowSensor(FlowSensor):
    measuresMedium: Medium = Air
    unit: URIRef = unit["FT3-PER-MIN"]


class WaterFlowSensor(FlowSensor):
    measuresMedium: Medium = Water
    unit: URIRef = unit["GAL_UK-PER-MIN"]
