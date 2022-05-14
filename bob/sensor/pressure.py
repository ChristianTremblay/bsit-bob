from typing import Any, List

from rdflib import URIRef

from bob import core
from bob.connections.electricity import OnOffSignalOutletConnectionPoint

from ..core import (
    Air,
    ExternalReference,
    Medium,
    Node,
    PropertyReference,
    Water,
    enum,
    p223,
    quantitykind,
    unit,
)
from ..properties import DifferentialStaticPressure
from ..property import QuantifiableProperty, Setpoint
from .sensor import Sensor, split_kwargs

_namespace = p223


class DifferentialStaticPressureSetpoint(Setpoint):
    hasQuantityKind: URIRef = quantitykind.ForcePerArea
    unit: URIRef


class DifferentialStaticPressureSensor(Sensor):
    observesProperty: PropertyReference  # DifferentialStaticPressure
    hasMeasurementLocationHigh: Node  # I don't know how to type a list of 2 nodes...
    hasMeasurementLocationLow: Node

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observesProperty = DifferentialStaticPressure(
            # isObservedBy=self,
            label=f"{self.label}.DifferentialStaticPressure",
            **_property_kwargs,
        )


class AirDifferentialStaticPressureSensor(DifferentialStaticPressureSensor):
    def __init__(self, **kwargs):
        super().__init__(ofMedium=Air, **kwargs)


class WaterDifferentialStaticPressureSensor(DifferentialStaticPressureSensor):
    def __init__(self, **kwargs):
        super().__init__(ofMedium=Water, **kwargs)
