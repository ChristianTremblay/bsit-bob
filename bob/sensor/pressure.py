from .sensor import Sensor, Measurement, QuantifiableMeasurement, split_kwargs
from rdflib import URIRef
from typing import Any, List
from ..core import quantitykind, s223, p223, unit, enum, Medium, Node

from ..property import QuantifiableObservableProperty, QuantifiableProperty

from bob import core

__namespace__ = s223


class DifferentialStaticPressureMeasure(QuantifiableMeasurement):
    node_type: URIRef = p223.Measure
    hasQuantityKind: URIRef = quantitykind.ForcePerArea
    unit: URIRef = unit.PA
    # isObservedBy: Sensor
    ofSubstance: Medium


class DifferentialStaticPressureSetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.ForcePerArea
    unit: URIRef = unit.PA


class DifferentialStaticPressureSensor(Sensor):
    node_type: URIRef = s223.DifferentialSensor
    observesProperty: DifferentialStaticPressureMeasure
    measuresSubstance: URIRef = s223["Medium-Air"]
    hasMeasurementLocationHigh: Node  # I don't know how to type a list of 2 nodes...
    hasMeasurementLocationLow: Node

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        _measure = DifferentialStaticPressureMeasure(
            ofSubstance=self.measuresSubstance,
            # isObservedBy=self,
            label=f"{self.label}.Measure",
            **_measure_kwargs,
        )
        self.observesProperty = _measure
