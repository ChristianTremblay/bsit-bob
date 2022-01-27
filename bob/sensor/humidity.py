from __future__ import annotations

from typing import Any
from rdflib import URIRef

from ..core import s223, enum, quantitykind, unit

from .sensor import Sensor

from ..property import (
    ObservableProperty,
    QuantifiableProperty,
    QuantifiableObservableProperty,
)

__namespace__ = s223


class HumidityMeasure(QuantifiableObservableProperty):
    node_type: URIRef = s223.HumidityMeasure
    hasQuantityKind: URIRef = quantitykind.RelativeHumidity
    # whew.... RelativeHumidity would have make sense here...
    # looks like something to talk with Steve Ray
    hasUnit: URIRef = unit.PERCENT_RH


class HumiditySetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.RelativeHumidity
    hasUnit: URIRef = unit.PERCENT_RH


class AirHumiditySensor(Sensor):
    """
    Air humidity sensor. Can model room sensor or duct sensor
    """

    node_type: URIRef = s223.HumiditySensor
    hasSubstance: URIRef = enum["Medium-Air"]
    hasQuantityKind: URIRef = quantitykind.RelativeHumidity
    observesProperty: HumidityMeasure

    def __init__(self, **kwargs: Any) -> None:

        if "extref" in kwargs:
            _measure = HumidityMeasure(hasExternalReference=kwargs.pop("extref"))
        elif "value" in kwargs:
            _measure = HumidityMeasure(hasValue=kwargs.pop("value"))
        else:
            _measure = HumidityMeasure()

        super().__init__(**kwargs)
        self.observesProperty = _measure
