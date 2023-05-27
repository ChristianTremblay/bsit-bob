from __future__ import annotations

from typing import Any

from rdflib import URIRef

from ..core import (
    BOB,
    P223,
    QUANTITYKIND,
    S223,
    UNIT,
    Air,
    EnumerationKind,
    Equipment,
    Medium,
    Node,
    PropertyReference,
    Substance,
)
from ..properties import GasConcentration
from ..property import QuantifiableProperty, Setpoint
from .sensor import Sensor, split_kwargs

_namespace = BOB

# TODO :
# try to create an exmaple for the sensors found here
# Sal will like :0)
# And those are from Quebec
# http://operadetectors.com/category/gas-monitors-1.aspx


class GasConcentrationSetpoint(Setpoint):
    _class_iri = S223.Setpoint
    hasQuantityKind: URIRef = QUANTITYKIND.DimensionlessRatio
    unit: URIRef = UNIT.PPM


class GasConcentrationSensor(Sensor):
    _class_iri = S223.Sensor
    observes: PropertyReference  # GasConcentration
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "ofSubstance" not in _property_kwargs:
            raise ValueError(
                "You must provide ofSubstance when defining a gas concentration sensor"
            )

        super().__init__(**_sensor_kwargs)

        self.observes = GasConcentration(
            # isObservedBy=self,
            label=f"{self.label}.GasConcentration",  # needs more focus
            **_property_kwargs,
        )


class CO2Sensor(GasConcentrationSensor):
    _class_iri = S223.Sensor
    "Carbon Dioxide concentration sensor"
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, **kwargs):
        # _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(ofSubstance=Substance.CO2, **kwargs)


class COSensor(GasConcentrationSensor):
    _class_iri = S223.Sensor
    "Carbon monoxide concentration sensor"
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, **kwargs):
        # _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(ofSubstance=Substance.CO, **kwargs)


class NO2Sensor(GasConcentrationSensor):
    _class_iri = S223.Sensor
    "Diesel (NO2) concentration sensor"
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, **kwargs):
        # _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(ofSubstance=Substance.NO2, **kwargs)


class CH4Sensor(GasConcentrationSensor):
    _class_iri = S223.Sensor
    "Natural gas sensor"
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, **kwargs):
        # _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(ofSubstance=Substance.CH4, **kwargs)
