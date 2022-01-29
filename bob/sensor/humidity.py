from __future__ import annotations

from typing import Any
from rdflib import URIRef

from ..core import s223, enum, quantitykind, unit, Medium

from .sensor import Sensor, QuantifiableMeasurement

from ..property import (
    ObservableProperty,
    QuantifiableProperty,
    QuantifiableObservableProperty,
)

__namespace__ = s223


class HumidityMeasure(QuantifiableMeasurement):
    node_type: URIRef = s223.HumidityMeasure
    hasQuantityKind: URIRef = quantitykind.RelativeHumidity
    # whew.... RelativeHumidity would have make sense here...
    # looks like something to talk with Steve Ray
    unit: URIRef = unit.PERCENT_RH
    # measuresSubstance: URIRef = enum['Medium-Air']
    # isObservedBy: Sensor
    ofSubstance: Medium


class HumiditySetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.RelativeHumidity
    unit: URIRef = unit.PERCENT_RH


class AirHumiditySensor(Sensor):
    """
    Air humidity sensor. Can model room sensor or duct sensor
    """

    node_type: URIRef = s223.HumiditySensor
    hasSubstance: URIRef = enum["Medium-Air"]
    hasQuantityKind: URIRef = quantitykind.RelativeHumidity
    observesProperty: HumidityMeasure
    measuresSubstance: URIRef = enum["Medium-Air"]

    def __init__(self, **kwargs: Any) -> None:
        _refs = None
        _val = None
        if "extref" in kwargs:
            _refs = kwargs.pop("extref")

        elif "value" in kwargs:
            _val = kwargs.pop("value")

        super().__init__(**kwargs)
        _measure = HumidityMeasure(
            hasExternalReference=_refs,
            hasValue=_val,
            ofSubstance=self.measuresSubstance,
            isObservedBy=self,
        )

        self.observesProperty = _measure
