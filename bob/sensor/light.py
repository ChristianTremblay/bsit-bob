from typing import Any

from rdflib import URIRef

from bob import core
from bob.properties.states import DaylightDetected, OnOffStatus

from ..core import (
    ExternalReference,
    Light,
    Medium,
    PropertyReference,
    BOB,
    P223,
    QUANTITYKIND,
    S223,
    UNIT,
)
from ..properties import Movement
from .sensor import Sensor, split_kwargs

_namespace = BOB


class MovementSensor(Sensor):
    _class_iri = S223.Sensor
    # measuresMedium: Medium = Light
    observesProperty: PropertyReference  # Movement

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observesProperty = Movement(
            # isObservedBy=self,
            label=f"{self.label}.Movement",
            ofMedium=Light,
            **_property_kwargs,
        )


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


class OccupancySensor(MovementSensor):
    _class_iri = S223.Sensor


class IntrusionSensor(Sensor):
    _class_iri = S223.Sensor
    # measuresMedium: Medium = Light
    observesProperty: PropertyReference  # Intrusion...good for Windows and doors

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        self.observesProperty = OnOffStatus(
            # isObservedBy=self,
            label=f"{self.label}.Intrusion",
            **_measure_kwargs,
        )
