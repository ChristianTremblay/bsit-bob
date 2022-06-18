from __future__ import annotations

from typing import Any

from rdflib import URIRef

from ..core import (
    Air,
    Medium,
    PropertyReference,
    bob,
    enum,
    p223,
    quantitykind,
    s223,
    unit,
)
from ..properties import RelativeHumidity
from ..property import (
    ObservableProperty,
    QuantifiableObservableProperty,
    QuantifiableProperty,
    Setpoint,
)
from .sensor import Sensor, split_kwargs

_namespace = bob


class HumiditySetpoint(Setpoint):
    _class_iri = s223.Setpoint
    hasQuantityKind: URIRef = quantitykind.RelativeHumidity
    unit: URIRef = unit.PERCENT_RH


class AirHumiditySensor(Sensor):
    """
    Air humidity sensor. Can model room sensor or duct sensor.
    """

    _class_iri = s223.Sensor

    # measuresMedium: Medium = Air
    hasQuantityKind: URIRef = quantitykind.RelativeHumidity
    observesProperty: PropertyReference  # Humidity

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observesProperty = RelativeHumidity(
            # isObservedBy=self,
            label=f"{self.label}.Measure",
            # ofMedium=Air,  -- RelativeHumidity already knows this
            **_property_kwargs,
        )
