from ..properties.states import OnOffStatus
from .sensor import Sensor, QuantifiableMeasuredProperty, split_kwargs
from rdflib import URIRef
from typing import Any
from ..core import (
    Electricity,
    quantitykind,
    p223,
    unit,
    Medium,
    Air,
    Water,
    PropertyReference,
    Node,
)

from ..property import ObservableProperty, QuantifiableProperty

__namespace__ = p223


class VoltageAN(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.Voltage
    unit: URIRef = unit.V
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor


class VoltageBN(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.Voltage
    unit: URIRef = unit.V
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor


class VoltageCN(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.Voltage
    unit: URIRef = unit.V
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor


class VoltageAB(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.Voltage
    unit: URIRef = unit.V
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor


class VoltageBC(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.Voltage
    unit: URIRef = unit.V
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor


class VoltageAC(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.Voltage
    unit: URIRef = unit.V
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor


class CurrentPhaseA(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.ElectricCurrent
    unit: URIRef = unit.A
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor


class CurrentPhaseB(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.ElectricCurrent
    unit: URIRef = unit.A
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor


class CurrentPhaseC(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.ElectricCurrent
    unit: URIRef = unit.A
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor


class Frequency(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.Frequency
    measuresMedium: Medium  # set from the sensor
    unit: URIRef = unit.HZ
    measuresMedium: Medium  # set from the sensor
    # isObservedBy: Sensor


class ElectricalPower(QuantifiableMeasuredProperty):
    hasQuantityKind: URIRef = quantitykind.ElectricalPower
    measuresMedium: Medium  # set from the sensor
    unit: URIRef = unit.kW
    # isObservedBy: Sensor


class CurrentSwitch(OnOffStatus):
    measuresMedium: Medium  # set from the sensor


class VoltageSensor(Sensor):
    observesProperty: PropertyReference  # Voltage

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)
        _class = _sensor_kwargs.pop("measures")
        super().__init__(**_sensor_kwargs)
        if not self.measuresMedium:
            raise ValueError(
                "You must provide measuresMedium property for a temperature sensor either in config template or subclass defintion"
            )
        self.measure = _class(
            measuresMedium=self.measuresMedium,
            # isObservedBy=self,
            label=f"{self.label}.{_class.__name__}",
            **_measure_kwargs,
        )
        self.observesProperty = self.measure


class CurrentAnalogSensor(Sensor):
    observesProperty: PropertyReference  # Current

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)
        _class = _sensor_kwargs.pop("measures")
        super().__init__(**_sensor_kwargs)
        if not self.measuresMedium:
            raise ValueError(
                "You must provide measuresMedium property for a temperature sensor either in config template or subclass defintion"
            )
        self.measure = _class(
            measuresMedium=self.measuresMedium,
            # isObservedBy=self,
            label=f"{self.label}.{_class.__name__}",
            **_measure_kwargs,
        )
        self.observesProperty = self.measure


def create_3phases_meter_sensors(
    label: str = None,
    measuresMedium: Medium = None,
    hasMeasurementLocation: Node = None,
):
    voltage_sensors = [VoltageAB, VoltageAC, VoltageBC, VoltageAN, VoltageBN, VoltageCN]
    current_sensors = [CurrentPhaseA, CurrentPhaseB, CurrentPhaseC]
    v_sensors = []
    c_sensors = []

    sensors = {}
    for each in voltage_sensors:
        v_sensors.append(
            VoltageSensor(
                label=f"{label}_{each.__name__}",
                measures=each,
                measuresMedium=measuresMedium,
            )
        )
    for each in current_sensors:
        c_sensors.append(
            CurrentAnalogSensor(
                label=f"{label}_{each.__name__}",
                measures=each,
                measuresMedium=measuresMedium,
            )
        )

    sensors["voltage"] = v_sensors
    sensors["current"] = c_sensors

    return sensors


class CurrentBinarySensor(Sensor):
    measuresMedium: Medium = Electricity
    observesProperty: PropertyReference  # DifferentialStaticPressure
    hasMeasurementLocation: Node

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        self.measure = OnOffStatus(
            measuresMedium=self.measuresMedium,
            # isObservedBy=self,
            label=f"{self.label}.CurrentBinarySensor",
            **_measure_kwargs,
        )
        self.observesProperty = self.measure
