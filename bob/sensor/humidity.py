from __future__ import annotations

from typing import Any

from rdflib import URIRef

from ..core import (
    BOB,
    P223,
    QUANTITYKIND,
    S223,
    UNIT,
    Air,
    Medium,
    PropertyReference,
    enum,
)
from ..properties import RelativeHumidity
from ..property import (
    ObservableProperty,
    QuantifiableObservableProperty,
    QuantifiableProperty,
    Setpoint,
)
from .sensor import Sensor, split_kwargs

_namespace = BOB


class HumiditySetpoint(Setpoint):
    _class_iri = S223.Setpoint
    hasQuantityKind: URIRef = QUANTITYKIND.RelativeHumidity
    unit: URIRef = UNIT.PERCENT_RH


class AirHumiditySensor(Sensor):
    """
    Air humidity sensor. Can model room sensor or duct sensor.
    """

    _class_iri = S223.Sensor

    # measuresMedium: Medium = Air
    hasQuantityKind: URIRef = QUANTITYKIND.RelativeHumidity
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
