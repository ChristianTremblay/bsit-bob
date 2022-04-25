from typing import Dict

from ...connections.electricity import *
from ...core import Device, Node, p223, s223
from ...sensor.electricity import create_3phase_meter_sensors

_namespace = s223


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

        meter = ThreePhaseElectricalMeter(label="Meter#1", ofMedium=Electricity_575V_60Hz)
        meter["Meter#1_VoltageAB"]

    # optional : you can set hasMeasurementLocation intially:

        a = Electricity_575V_60HzConnection(label="A")
        meter = ThreePhaseElectricalMeter(label="Meter#1", ofMedium=Electricity_575V_60Hz, hasMeasurementLocation=a)

    # or later:

        meter.set_measurement_location(a)

    """

    node_type = s223.ElectricMeter

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        _label = kwargs["label"]
        _ofMedium = kwargs.pop("ofMedium")
        _hasMeasurementLocation = kwargs.pop("hasMeasurementLocation", None)

        super().__init__(**kwargs)

        self.voltage_sensors, self.current_sensors = create_3phase_meter_sensors(
            label=_label,
            ofMedium=_ofMedium,
            hasMeasurementLocation=_hasMeasurementLocation,
        )

        for each in self.voltage_sensors:
            self > each

        for each in self.current_sensors:
            self > each

    def set_measurement_location(self, node: Node = None):
        self.set_voltage_measurement_location(node)
        self.set_current_measurement_location(node)

    def set_voltage_measurement_location(self, node: Node = None):
        for each in self.voltage_sensors:
            each.hasMeasurementLocation = node

    def set_current_measurement_location(self, node: Node = None):
        for each in self.current_sensors:
            each.hasMeasurementLocation = node
