from __future__ import annotations

from typing import Any

from rdflib import URIRef

from ..core import (
    Air,
    EnumerationKind,
    Medium,
    Node,
    PropertyReference,
    Substance,
    p223,
    quantitykind,
    unit,
)
from ..properties import GasConcentration
from ..property import QuantifiableProperty, Setpoint
from .sensor import Sensor, split_kwargs

_namespace = p223

# TODO :
# try to create an exmaple for the sensors found here
# Sal will like :0)
# And those are from Quebec
# http://operadetectors.com/category/gas-monitors-1.aspx


class GasConcentrationSetpoint(Setpoint):
    hasQuantityKind: URIRef = quantitykind.DimensionlessRatio
    unit: URIRef = unit.PPM


class GasConcentrationSensor(Sensor):
    hasQuantityKind: URIRef = quantitykind.DimensionlessRatio
    observesProperty: PropertyReference  # GasConcentration

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "ofSubstance" not in _property_kwargs:
            raise ValueError(
                "You must provide ofSubstance when defining a gas concentration sensor"
            )

        super().__init__(**_sensor_kwargs)

        self.observesProperty = GasConcentration(
            # isObservedBy=self,
            label=f"{self.label}.GasConcentration",  # needs more focus
            **_property_kwargs,
        )


class CO2Sensor(GasConcentrationSensor):
    "Carbon Dioxide concentration sensor"
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, **kwargs):
        super().__init__(ofSubstance=Substance.CO2, **kwargs)


class COSensor(GasConcentrationSensor):
    "Carbon monoxide concentration sensor"
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, **kwargs):
        super().__init__(ofSubstance=Substance.CO, **kwargs)


class NO2Sensor(GasConcentrationSensor):
    "Diesel (NO2) concentration sensor"
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, **kwargs):
        super().__init__(ofSubstance=Substance.NO2, **kwargs)


class CH4Sensor(GasConcentrationSensor):
    "Natural gas sensor"
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, **kwargs):
        super().__init__(ofSubstance=Substance.CH4, **kwargs)
