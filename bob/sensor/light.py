from typing import Any

from rdflib import URIRef

from bob import core
from bob.connections.controlsignal import OnOffSignalOutletConnectionPoint
from bob.properties.states import DaylightDetected, OnOffStatus

from ..core import (
    BOB,
    P223,
    QUANTITYKIND,
    S223,
    UNIT,
    Equipment,
    ExternalReference,
    Medium,
    PropertyReference,
)
from .sensor import Sensor, split_kwargs
from ..enum import Light

_namespace = BOB


class DaylightSensor(Sensor):
    _class_iri = S223.Sensor
    # measuresMedium: Medium = Light
    observes: PropertyReference  # visible light level -- units?

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observes = DaylightDetected(
            # isObservedBy=self,
            label=f"{self.label}.Daylight",
            ofMedium=Light.Visible,
            **_property_kwargs,
        )
