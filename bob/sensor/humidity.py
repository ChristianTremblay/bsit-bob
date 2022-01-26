from __future__ import annotations

from typing import Any
from rdflib import URIRef

from ..core import s223, quantitykind, unit

from .sensor import Sensor

from ..property import (
    ObservableProperty,
    QuantifiableProperty,
    QuantifiableObservableProperty,
)

__namespace__ = s223


class HumidityMeasure(QuantifiableObservableProperty):
    node_type: URIRef = s223.HumidityMeasure
    hasQuantityKind: quantitykind.PressureRatio
    # whew.... RelativeHumidity would have make sense here...
    # looks like something to talk with Steve Ray
    hasUnit: unit.PERCENT_RH


class HumiditySetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.Temperature
    hasUnit: URIRef = unit.PERCENT_RH


class AirHumiditySensor(Sensor):
    node_type: URIRef = s223.HumiditySensor
    hasSubstance: URIRef = s223.Air
    hasQuantityKind: quantitykind.RelativeHumidity
    observesProperty: HumidityMeasure

    def __init__(self, **kwargs: Any) -> None:

        if "datasource" in kwargs:
            _measure = HumidityMeasure(hasExternalDataSource=kwargs.pop("datasource"))
        elif "value" in kwargs:
            _measure = HumidityMeasure(hasValue=kwargs.pop("value"))
        else:
            _measure = HumidityMeasure()

        super().__init__(**kwargs)
        self.observesProperty = _measure
