from bob.connections.electricity import OnOffSignalOutletConnectionPoint
from .sensor import Sensor, QuantifiableMeasuredProperty, split_kwargs
from rdflib import URIRef
from typing import Any, List
from ..core import quantitykind, p223, unit, enum, Medium, Air, Node, PropertyReference

from ..property import QuantifiableProperty

from bob import core

__namespace__ = p223


class DifferentialStaticPressure(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.ForcePerArea
    unit: URIRef = unit.PA
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor


class DifferentialStaticPressureSetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.ForcePerArea
    unit: URIRef = unit.PA


class DifferentialStaticPressureSensor(Sensor):
    measuresMedium: Medium = Air
    observesProperty: PropertyReference  # DifferentialStaticPressure
    hasMeasurementLocationHigh: Node  # I don't know how to type a list of 2 nodes...
    hasMeasurementLocationLow: Node
    dryContactOutlet: OnOffSignalOutletConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        _measure = DifferentialStaticPressure(
            measuresMedium=self.measuresMedium,
            # isObservedBy=self,
            label=f"{self.label}.DifferentialStaticPressure",
            **_measure_kwargs,
        )
        self.observesProperty = _measure
