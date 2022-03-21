from .sensor import Sensor, QuantifiableMeasuredProperty, split_kwargs
from rdflib import URIRef
from typing import Any
from ..core import (
    Substance,
    quantitykind,
    p223,
    unit,
    Medium,
    Air,
    Water,
    PropertyReference,
)

from ..property import QuantifiableProperty, Setpoint
from ..connections.electricity import OnOffSignalOutletConnectionPoint

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

        self.measure = SmokePresence(
            isObservedBy=self,
            label=f"{self.label}.SmokeDetection",  # needs more focus
            **_measure_kwargs,
        )
        self.observesProperty = self.measure
