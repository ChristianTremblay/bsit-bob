from typing import Any

from rdflib import URIRef

from ..connections.electricity import OnOffSignalOutletConnectionPoint
from ..core import (
    BOB,
    P223,
    QUANTITYKIND,
    S223,
    UNIT,
    Air,
    Equipment,
    Medium,
    PropertyReference,
    Substance,
    Water,
)
from ..properties import SmokePresence
from ..property import QuantifiableProperty, Setpoint
from .sensor import Sensor, split_kwargs

_namespace = BOB


class SmokeDetectionSensor(Sensor):
    _class_iri = S223.Sensor
    observes: PropertyReference  # Temperature
    dryContactOutlet: OnOffSignalOutletConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "unit" not in _property_kwargs:
            raise ValueError(
                "You must provide units when defining a smoke detection sensor"
            )
        if "ofMedium" not in _property_kwargs:
            raise ValueError(
                "You must provide ofMedium when defining a smoke detection sensor"
            )

        super().__init__(**_sensor_kwargs)

        self.observes = SmokePresence(
            # isObservedBy=self,
            label=f"{self.label}.SmokeDetection",
            ofMedium=Air,
            **_property_kwargs,
        )
