from .sensor import Sensor
from rdflib import URIRef
from typing import Any
from ..core import quantitykind, s223, unit, enum

from ..property import QuantifiableObservableProperty, QuantifiableProperty


__namespace__ = s223


class TemperatureMeasure(QuantifiableObservableProperty):
    node_type: URIRef = s223.TemperatureMeasure
    hasQuantityKind: URIRef = quantitykind.Temperature
    hasUnit: URIRef = unit.DEG_C


class TemperatureSetpoint(QuantifiableProperty):
    hasQuantityKind: URIRef = quantitykind.Temperature
    hasUnit: URIRef = unit.DEG_C


class TemperatureSensor(Sensor):
    node_type: URIRef = s223.TemperatureSensor
    observesProperty: TemperatureMeasure

    def __init__(self, **kwargs: Any) -> None:

        if "datasource" in kwargs:
            _measure = TemperatureMeasure(
                hasExternalDataSource=kwargs.pop("datasource")
            )
        elif "value" in kwargs:
            _measure = TemperatureMeasure(hasValue=kwargs.pop("value"))
        else:
            _measure = TemperatureMeasure()

        super().__init__(**kwargs)
        self.observesProperty = _measure


class AirTemperatureSensor(TemperatureSensor):
    hasSubstance: URIRef = enum.Medium_Air


class WaterTemperatureSensor(TemperatureSensor):
    hasSubstance: URIRef = enum.Medium_Water
