from typing import Any, List

from rdflib import URIRef

from bob import core
from bob.connections.controlsignal import OnOffSignalOutletConnectionPoint
from bob.producer.causality import Differential

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

_namespace = BOB  #


class PressureSensor(Sensor):
    _class_iri = S223.Sensor
    observes: PropertyReference  # Temperature
    hasObservationLocation: LocationReference

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "hasUnit" not in _property_kwargs:
            raise ValueError("You must provide hasUnit when defining a pressure sensor")
        if "ofMedium" not in _property_kwargs:
            raise ValueError(
                "You must provide ofMedium when defining a pressure sensor"
            )

        super().__init__(**_sensor_kwargs)

        self.observes = DifferentialStaticPressure(
            # isObservedBy=self,
            label=f"{self.label}.DifferentialStaticPressure",
            **_property_kwargs,
        )


class DifferentialStaticPressureSetpoint(Setpoint):
    _class_iri = S223.Sensor
    hasQuantityKind: URIRef = QUANTITYKIND.ForcePerArea
    hasUnit: URIRef


class DifferentialStaticPressureSensor(Sensor):
    _class_iri = S223.DifferentialSensor

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)


class AirDifferentialStaticPressureSensor(Sensor):
    _class_iri = S223.DifferentialSensor
    # observes: PropertyReference
    differential_static_pressure: DifferentialStaticPressure

    def __init__(self, **kwargs):
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(**_sensor_kwargs)
        self.differential_static_pressure = DifferentialStaticPressure(
            ofMedium=Air,
            label=f"{self.label}.DifferentialStaticPressure",
            **_property_kwargs,
        )
        self > PressureSensor(label=f"highPort", ofMedium=Air, **_property_kwargs)
        self > PressureSensor(label=f"lowPort", ofMedium=Air, **_property_kwargs)
        self > Differential(
            label="diff_causality", comment="Will output High minus Low"
        )
        self["highPort"].observedProperty >> self["diff_causality"].high_input
        self["lowPort"].observedProperty >> self["diff_causality"].low_input
        self["diff_causality"].differential_output >> self.differential_static_pressure
        self.observes = self.differential_static_pressure


class WaterDifferentialStaticPressureSensor(DifferentialStaticPressureSensor):
    _class_iri = S223.DifferentialSensor
    differential_static_pressure: DifferentialStaticPressure

    def __init__(self, **kwargs):
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(**_sensor_kwargs)
        self.differential_static_pressure = DifferentialStaticPressure(
            ofMedium=Water,
            label=f"{self.label}.DifferentialStaticPressure",
            **_property_kwargs,
        )
        self > PressureSensor(label=f"highPort", ofMedium=Water, **_property_kwargs)
        self > PressureSensor(label=f"lowPort", ofMedium=Water, **_property_kwargs)
        self > Differential(label="output", comment="Will output High minus Low")
        self["highPort"].observes >> self["output"].high
        self["lowPort"].observes >> self["output"].low
        self["output"].differential >> self.differential_static_pressure
        self.observes = self.differential_static_pressure
