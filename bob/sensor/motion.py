from typing import Any

from rdflib import URIRef

from bob import core
from bob.connections.electricity import OnOffSignalOutletConnectionPoint
from bob.properties.states import DaylightDetected, OnOffStatus

from ..core import (
    BOB,
    P223,
    QUANTITYKIND,
    S223,
    UNIT,
    ExternalReference,
    Medium,
    Occupant,
    PropertyReference,
)
from ..properties import Count, Motion
from .sensor import Sensor, split_kwargs

_namespace = S223


class OccupancySensor(Sensor):
    _class_iri = S223.OccupancySensor


class PersonMotionSensor(OccupancySensor):
    _class_iri = S223.PersonMotionSensor
    # measuresMedium: Medium = Light
    observesProperty: PropertyReference  # Movement

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observesProperty = Motion(
            # isObservedBy=self,
            label=f"{self.label}.PersonMotion",
            ofMedium=Occupant,
            **_property_kwargs,
        )


class PersonCounter(OccupancySensor):
    _class_iri = S223.PersonCounter
    # measuresMedium: Medium = Light
    observesProperty: PropertyReference  # Count

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observesProperty = Count(
            label=f"{self.label}.PersonCount",
            ofMedium=Occupant,
            **_property_kwargs,
        )


class PersonPresenceSensor(Sensor):
    _class_iri = S223.Sensor
    # measuresMedium: Medium = Light
    observesProperty: PropertyReference  # Intrusion...good for Windows and doors
    onoff_contact: OnOffSignalOutletConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        self.observesProperty = OnOffStatus(
            # isObservedBy=self,
            label=f"{self.label}.PersonPresence",
            **_measure_kwargs,
        )
