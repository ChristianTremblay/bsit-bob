from typing import Any

from rdflib import URIRef

from ..connections.electricity import OnOffSignalOutletConnectionPoint
from ..core import (
    Air,
    Medium,
    PropertyReference,
    Substance,
    Water,
    p223,
    quantitykind,
    unit,
)
from ..property import QuantifiableProperty, Setpoint
from .sensor import QuantifiableMeasuredProperty, Sensor, split_kwargs

__namespace__ = p223

Smoke = Substance(node_iri=p223["Substance-Smoke"])


class SmokePresence(QuantifiableMeasuredProperty):
    measuresMedium: Medium  # set from the sensor
    measuresSubstance: Substance = Smoke
    # isObservedBy: Sensor


class SmokeDetectionSensor(Sensor):
    measuresMedium: Medium = Air
    observesProperty: PropertyReference
    dryContactOutlet: OnOffSignalOutletConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)
        super().__init__(**_sensor_kwargs)

        self.observesProperty = SmokePresence(
            isObservedBy=self,
            label=f"{self.label}.SmokeDetection",  # needs more focus
            **_measure_kwargs,
        )
