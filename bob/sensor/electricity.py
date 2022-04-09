from typing import Any

from rdflib import URIRef

from ..core import (
    Air,
    Electricity,
    Medium,
    Node,
    PropertyReference,
    Water,
    quantitykind,
    s223,
    unit,
)
from ..properties import Amps, OnOffStatus, Volts
from ..property import ObservableProperty, QuantifiableProperty
from .sensor import Sensor, split_kwargs

__namespace__ = s223


class CurrentSwitch(OnOffStatus):
    measuresMedium: Medium  # set from the sensor


class VoltageSensor(Sensor):
    observesProperty: PropertyReference  # Voltage

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)
        _class = _sensor_kwargs.pop("measures")
        super().__init__(**_sensor_kwargs)
        self.observesProperty = _class(
            # isObservedBy=self,
            label=f"{self.label}.{_class.__name__}",
            **_measure_kwargs,
        )


class CurrentAnalogSensor(Sensor):
    observesProperty: PropertyReference  # Current

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)
        _class = _sensor_kwargs.pop("measures")
        super().__init__(**_sensor_kwargs)
        self.observesProperty = _class(
            # isObservedBy=self,
            label=f"{self.label}.{_class.__name__}",
            **_measure_kwargs,
        )


def create_3phase_meter_sensors(
    label: str = None,
    measuresMedium: Medium = None,
    hasMeasurementLocation: Node = None,
):
    voltage_sensors = [
        "VoltageAB",
        "VoltageAC",
        "VoltageBC",
        "VoltageAN",
        "VoltageBN",
        "VoltageCN",
    ]
    current_sensors = ["CurrentPhaseA", "CurrentPhaseB", "CurrentPhaseC"]

    v_sensors = []
    for each in voltage_sensors:
        v_sensors.append(
            VoltageSensor(
                label=f"{label}_{each}",
                measures=Volts(label=each),
                measuresMedium=measuresMedium,
            )
        )

    c_sensors = []
    for each in current_sensors:
        c_sensors.append(
            CurrentAnalogSensor(
                label=f"{label}_{each}",
                measures=Amps(label=each),
                measuresMedium=measuresMedium,
            )
        )

    return (v_sensors, c_sensors)


class CurrentBinarySensor(Sensor):
    observesProperty: PropertyReference  # Electrical Current
    hasMeasurementLocation: Node

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        self.observesProperty = OnOffStatus(
            # isObservedBy=self,
            label=f"{self.label}.CurrentBinarySensor",
            **_measure_kwargs,
        )
