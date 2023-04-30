from typing import Any

from bob.properties.states import OnOffStatus

from ..core import (
    BOB,
    P223,
    QUANTITYKIND,
    S223,
    UNIT,
    Equipment,
    ExternalReference,
    Medium,
    Occupant,
    PropertyReference,
)
from ..properties import Count, Motion
from .sensor import Sensor, split_kwargs

_namespace = S223


class IntrusionSensor(OnOffStatus):
    _class_iri = P223.IntrusionSensor

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**kwargs)
        # self > OnOffStatus(label=f"{self.label}.sensor", **_property_kwargs)
