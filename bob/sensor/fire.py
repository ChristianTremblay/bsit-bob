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
    observesProperty: PropertyReference
    dryContactOutlet: OnOffSignalOutletConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observesProperty = SmokePresence(
            isObservedBy=self,
            label=f"{self.label}.SmokeDetection",  # needs more focus
            ofMedium=Air,
            **_property_kwargs,
        )
