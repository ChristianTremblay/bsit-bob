from typing import Any

from rdflib import URIRef

from bob import core
from bob.properties.states import DaylightDetected, OnOffStatus
from bob.connections.electricity import OnOffSignalOutletConnectionPoint

from ..core import (
    BOB,
    P223,
    QUANTITYKIND,
    S223,
    UNIT,
    ExternalReference,
    Light,
    Medium,
    PropertyReference,
)
from ..properties import Motion
from .sensor import Sensor, split_kwargs

_namespace = BOB


class DaylightSensor(Sensor):
    _class_iri = S223.Sensor
    # measuresMedium: Medium = Light
    observesProperty: PropertyReference  # Movement

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observesProperty = DaylightDetected(
            # isObservedBy=self,
            label=f"{self.label}.Daylight",
            ofMedium=Light.Visible,
            **_property_kwargs,
        )
