from bob.connections.electricity import OnOffSignalOutletConnectionPoint
from .sensor import Sensor, QuantifiableMeasuredProperty, split_kwargs
from rdflib import URIRef
from typing import Any, List
from ..core import (
    ExternalReference,
    quantitykind,
    p223,
    unit,
    enum,
    Medium,
    Air,
    Water,
    Node,
    PropertyReference,
)

from ..property import QuantifiableProperty

from bob import core

__namespace__ = p223


class DifferentialStaticPressure(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.ForcePerArea
    unit: URIRef
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor


class DifferentialStaticPressureSetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.ForcePerArea
    unit: URIRef


class DifferentialStaticPressureSensor(Sensor):
    measuresMedium: Medium = Air
    observesProperty: PropertyReference  # DifferentialStaticPressure
    hasMeasurementLocationHigh: Node  # I don't know how to type a list of 2 nodes...
    hasMeasurementLocationLow: Node

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        self.observesProperty = DifferentialStaticPressure(
            # isObservedBy=self,
            label=f"{self.label}.DifferentialStaticPressure",
            **_measure_kwargs,
        )


class AirDifferentialStaticPressureSensor(DifferentialStaticPressureSensor):
    def __init__(self, **kwargs):
        super().__init__(measuresMedium=Air, unit=unit.PA, **kwargs)


class WaterDifferentialStaticPressureSensor(DifferentialStaticPressureSensor):
    def __init__(self, **kwargs):
        super().__init__(measuresMedium=Water, unit=unit.PSI, **kwargs)
