from typing import Any, List

from rdflib import URIRef

from bob import core
from bob.connections.electricity import OnOffSignalOutletConnectionPoint

from ..core import (
    BOB,
    P223,
    QUANTITYKIND,
    S223,
    UNIT,
    Air,
    ExternalReference,
    LocationReference,
    Medium,
    Node,
    PropertyReference,
    Water,
    enum,
)
from ..properties import DifferentialStaticPressure
from ..property import QuantifiableProperty, Setpoint
from .sensor import Sensor, split_kwargs

_namespace = BOB


class DifferentialStaticPressureSetpoint(Setpoint):
    _class_iri = S223.Sensor
    hasQuantityKind: URIRef = QUANTITYKIND.ForcePerArea
    unit: URIRef


class DifferentialStaticPressureSensor(Sensor):
    _class_iri = S223.Sensor
    observesProperty: PropertyReference  # DifferentialStaticPressure
    hasMeasurementLocationHigh: LocationReference
    hasMeasurementLocationLow: LocationReference

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observesProperty = DifferentialStaticPressure(
            # isObservedBy=self,
            label=f"{self.label}.DifferentialStaticPressure",
            **_property_kwargs,
        )


class AirDifferentialStaticPressureSensor(DifferentialStaticPressureSensor):
    _class_iri = S223.Sensor

    def __init__(self, **kwargs):
        super().__init__(ofMedium=Air, **kwargs)


class WaterDifferentialStaticPressureSensor(DifferentialStaticPressureSensor):
    _class_iri = S223.Sensor

    def __init__(self, **kwargs):
        super().__init__(ofMedium=Water, **kwargs)
