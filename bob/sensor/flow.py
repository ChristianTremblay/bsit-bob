from typing import Any

from rdflib import URIRef

from bob import core

from ..core import (
    Air,
    Medium,
    PropertyReference,
    Water,
    BOB,
    enum,
    P223,
    QUANTITYKIND,
    S223,
    UNIT,
)
from ..properties import Flow
from ..property import QuantifiableProperty, Setpoint
from .sensor import Sensor, split_kwargs

_namespace = BOB


class FlowSetpoint(Setpoint):
    _class_iri = S223.Setpoint
    hasQuantityKind: URIRef = QUANTITYKIND.VolumeFlowRate
    unit: URIRef


class FlowSensor(Sensor):
    _class_iri = S223.Sensor
    observesProperty: PropertyReference  # Flow

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observesProperty = Flow(
            # isObservedBy=self,
            label=f"{self.label}.Flow",
            **_property_kwargs,
        )


class AirFlowSensor(FlowSensor):
    _class_iri = S223.Sensor
    # typical unit : unit=UNIT["FT3-PER-MIN"]
    def __init__(self, **kwargs):
        super().__init__(ofMedium=Air, **kwargs)


class WaterFlowSensor(FlowSensor):
    _class_iri = S223.Sensor
    # typical unit : unit=UNIT["GAL_UK-PER-MIN"]
    def __init__(self, **kwargs):
        super().__init__(ofMedium=Water, **kwargs)
