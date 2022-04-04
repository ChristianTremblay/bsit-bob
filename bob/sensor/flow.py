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

__namespace__ = s223


class Flow(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.VolumeFlowRate
    unit: URIRef
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor


class FlowSetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.VolumeFlowRate
    unit: URIRef


class FlowSensor(Sensor):
    node_type: URIRef = p223.FlowSensor
    observesProperty: PropertyReference  # Flow

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        self.observesProperty = Flow(
            # isObservedBy=self,
            label=f"{self.label}.Flow",
            **_measure_kwargs,
        )


class AirFlowSensor(FlowSensor):
    node_type: URIRef = p223.AirFlowSensor

    def __init__(self, **kwargs):
        super().__init__(measuresMedium=Air, unit=unit["FT3-PER-MIN"], **kwargs)


class WaterFlowSensor(FlowSensor):
    node_type: URIRef = p223.WaterFlowSensor

    def __init__(self, **kwargs):
        super().__init__(measuresMedium=Water, unit=unit["GAL_UK-PER-MIN"], **kwargs)
