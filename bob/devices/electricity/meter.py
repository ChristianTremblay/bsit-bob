from ...connections.electricity import *
from ...sensor.electricity import create_3phase_meter_sensors

from ...core import Device, Node, s223, p223
from ...devices import composite
from typing import Any

__namespace__ = s223


class ThreePhaseElectricalMeter(Device):
    """
    This is an attemp to model a complete Electrical meter
    starting with all the voltages and current sensors.
    All other information being results
    of calculation based on those measures.

    To create one, you must specify a medium and a label
    Sensors will be added to the Meter device and be available
    by square bracket requests.

    ex. :

        meter = ThreePhaseElectricalMeter(label="Meter#1", measuresMedium=Electricity_575V_60Hz)
        meter["Meter#1_VoltageAB"]

    #optional : you can set hasMeasurementLocation intially:

        a = Electricity_575V_60HzConnection(label="A")
        meter = ThreePhaseElectricalMeter(label="Meter#1", measuresMedium=Electricity_575V_60Hz, hasMeasurementLocation=a)

    # or later:

        meter.set_hasMeasurementLocation(a)

    """

    node_type = s223.ElectricMeter

    def __init__(self, **kwargs):
        _measuresMedium = kwargs.pop("measuresMedium")
        _label = kwargs["label"]
        _hasMeasurementLocation = (
            kwargs.pop("hasMeasurementLocation")
            if "hasMeasurementLocation" in kwargs
            else None
        )
        super().__init__(**kwargs)
        _sensors = create_3phase_meter_sensors(
            label=_label,
            measuresMedium=_measuresMedium,
            hasMeasurementLocation=_hasMeasurementLocation,
        )
        self.voltage_sensors = _sensors["voltage"]
        self.current_sensors = _sensors["current"]

    def finalize(self):
        for each in self.voltage_sensors:
            self > each

        for each in self.current_sensors:
            self > each
        return self

    def set_hasMeasurementLocation(self, node: Node = None):
        self.voltage_hasMeasurementLocation(node)
        self.current_hasMeasurementLocation(node)

    def voltage_hasMeasurementLocation(self, node: Node = None):
        for each in self.voltage_sensors:
            each.hasMeasurementLocation = node

    def current_hasMeasurementLocation(self, node: Node = None):
        for each in self.voltage_sensors:
            each.hasMeasurementLocation = node

    def __getitem__(self, name: str) -> Any:
        for each in self._sensors:
            if each.label == name:
                return each
