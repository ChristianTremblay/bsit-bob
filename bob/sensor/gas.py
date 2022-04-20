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


CO = Substance(node_iri=p223["Substance-CO"])
CO2 = Substance(node_iri=p223["Substance-CO2"])
NO2 = Substance(node_iri=p223["Substance-NO2"])
CH4 = Substance(node_iri=p223["Substance-CH4"])


class GasConcentrationSetpoint(Setpoint):
    hasQuantityKind: URIRef = quantitykind.DimensionlessRatio
    unit: URIRef = unit.PPM


class GasConcentrationSensor(Sensor):
    hasQuantityKind: URIRef = quantitykind.DimensionlessRatio
    measuresMedium: Medium = Air
    observesProperty: PropertyReference  # GasConcentration

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)
        super().__init__(**_sensor_kwargs)

        if not self.measuresSubstance:
            raise ValueError(
                "You must provide measuresSubstance property for a gas concentration sensor either in config template or subclass defintion"
            )

        self.observesProperty = GasConcentration(
            measuresSubstance=self.measuresSubstance,
            isObservedBy=self,
            label=f"{self.label}.GasConcentration",  # needs more focus
            **_measure_kwargs,
        )


class CO2Sensor(GasConcentrationSensor):
    "Carbon Dioxide concentration sensor"
    measuresSubstance: Substance = CO2


class COSensor(GasConcentrationSensor):
    "Carbon monoxide concentration sensor"
    measuresSubstance: Substance = CO


class NO2Sensor(GasConcentrationSensor):
    "Diesel (NO2) concentration sensor"
    measuresSubstance: Substance = NO2


class CH4Sensor(GasConcentrationSensor):
    "Natural gas sensor"
    measuresSubstance: Substance = CH4
