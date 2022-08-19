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
from .motion import MotionSensor

_namespace = BOB


class DaylightSensor(Sensor):
    _class_iri = S223.Sensor
    # measuresMedium: Medium = Light
    observesProperty: PropertyReference  # visible light level -- units?

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observesProperty = DaylightDetected(
            # isObservedBy=self,
            label=f"{self.label}.Daylight",
            ofMedium=Light.Visible,
            **_property_kwargs,
        )


class OccupancySensor(MotionSensor):
    _class_iri = S223.Sensor


class IntrusionSensor(Sensor):
    _class_iri = S223.Sensor
    # measuresMedium: Medium = Light
    observesProperty: PropertyReference  # Intrusion...good for Windows and doors
    onoff_contact: OnOffSignalOutletConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        self.observesProperty = OnOffStatus(
            # isObservedBy=self,
            label=f"{self.label}.Intrusion",
            **_measure_kwargs,
        )
