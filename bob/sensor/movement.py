from typing import Any

from rdflib import URIRef

from bob import core
from bob.properties.states import OnOffStatus

from ..core import (
    ExternalReference,
    Light,
    Medium,
    PropertyReference,
    p223,
    quantitykind,
    unit,
)
from ..properties import Movement
from .sensor import Sensor, split_kwargs

_namespace = p223


class MovementSensor(Sensor):
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


class OccupancySensor(MovementSensor):
    _class_iri: URIRef = p223.OccupancySensor


class IntrusionSensor(Sensor):
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
