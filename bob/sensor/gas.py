from __future__ import annotations

from typing import Any
from rdflib import URIRef

from ..core import (
    p223,
    quantitykind,
    unit,
    Node,
    PropertyReference,
    EnumerationKind,
    Medium,
    Air,
    Substance,
)

from .sensor import Sensor, QuantifiableMeasuredProperty, split_kwargs

from ..property import (
    QuantifiableProperty,
)

__namespace__ = p223

# TODO :
# try to create an exmaple for the sensors found here
# Sal will like :0)
# And those are from Quebec
# http://operadetectors.com/category/gas-monitors-1.aspx


CO = Substance(node_iri=p223["Substance-CO"])
CO2 = Substance(node_iri=p223["Substance-CO2"])
NO2 = Substance(node_iri=p223["Substance-NO2"])
CH4 = Substance(node_iri=p223["Substance-CH4"])


class GasConcentration(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.DimensionlessRatio
    unit: URIRef = unit.PPM
    measuresMedium: Medium = Air
    measuresSubstance: Substance


class GasConcentrationSetpoint(QuantifiableProperty):
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

        self.measure = GasConcentration(
            measuresSubstance=self.measuresSubstance,
            isObservedBy=self,
            label=f"{self.label}.GasConcentration",  # needs more focus
            **_measure_kwargs,
        )
        self.observesProperty = self.measure


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
