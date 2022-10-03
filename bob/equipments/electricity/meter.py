from typing import Dict

from bob.properties import electricity
from bob.properties.electricity import (
    ElectricApparentEnergy,
    ElectricApparentPower,
    ElectricEnergy,
    ElectricPower,
    ElectricReactiveEnergy,
    ElectricReactivePower,
    Frequency,
    PowerFactor,
    Volts,
)
from bob.sensor.electricity import CurrentAnalogSensor, VoltageSensor

from ...connections.electricity import *
from ...core import BOB, P223, S223, UNIT, Device, Node, template_update

_namespace = BOB

three_phase_electricalmeter_template = {
    "properties": {
        ("energy", ElectricEnergy): {
            "unit": UNIT["KiloW-HR"],
            "comment": "Real Energy Consumption",
        },
        ("kW_total", ElectricPower): {
            "unit": UNIT["KiloW"],
            "comment": "Total Real Power",
        },
        ("kVAR_total", ElectricReactivePower): {
            "unit": UNIT["KiloV-A_Reactive"],
            "comment": "Total Reactive Power",
        },
        ("kVA_total", ElectricApparentPower): {
            "unit": UNIT["KiloV-A"],
            "comment": "Total Apparent Power",
        },
        ("power_factor", PowerFactor): {"comment": "Total Power Factor"},
        ("voltage_ll_avg", Volts): {"comment": "Voltage L-L Average"},
        ("voltage_ln_avg", Volts): {"comment": "Voltage L-N Average"},
        ("current_avg", Volts): {"comment": "Current Average"},
        ("kW_A", ElectricPower): {
            "unit": UNIT["KiloW"],
            "comment": "Real Power Phase A",
        },
        ("kW_B", ElectricPower): {
            "unit": UNIT["KiloW"],
            "comment": "Real Power Phase B",
        },
        ("kW_C", ElectricPower): {
            "unit": UNIT["KiloW"],
            "comment": "Real Power Phase C",
        },
        ("power_factor_A", PowerFactor): {"comment": "Power Factor Phase A"},
        ("power_factor_B", PowerFactor): {"comment": "Power Factor Phase B"},
        ("power_factor_C", PowerFactor): {"comment": "Power Factor Phase C"},
        ("frequency", Frequency): {"comment": "Frequency"},
        ("kVAh", ElectricApparentEnergy): {
            "unit": UNIT["KiloV-A-HR"],
            "comment": "Apparent Energy Consumption",
        },
        ("kVARh", ElectricReactiveEnergy): {
            "unit": UNIT["KiloV-A_Reactive-HR"],
            "comment": "Reactive Energy Consumption",
        },
        ("kVA_A", ElectricApparentPower): {
            "unit": UNIT["KiloV-A"],
            "comment": "Apparent Power Phase A",
        },
        ("kVA_B", ElectricApparentPower): {
            "unit": UNIT["KiloV-A"],
            "comment": "Apparent Power Phase B",
        },
        ("kVA_C", ElectricApparentPower): {
            "unit": UNIT["KiloV-A"],
            "comment": "Apparent Power Phase C",
        },
        ("kVAR_A", ElectricReactivePower): {
            "unit": UNIT["KiloV-A_Reactive"],
            "comment": "Reactive Power Phase A",
        },
        ("kVAR_B", ElectricReactivePower): {
            "unit": UNIT["KiloV-A_Reactive"],
            "comment": "Reactive Power Phase B",
        },
        ("kVAR_C", ElectricReactivePower): {
            "unit": UNIT["KiloV-A_Reactive"],
            "comment": "Reactive Power Phase C",
        },
        ("kW_present_demand", ElectricPower): {
            "unit": UNIT["KiloW"],
            "comment": "Total Real Power Present Demand",
        },
        ("kVAR_present_demand", ElectricReactivePower): {
            "unit": UNIT["KiloV-A_Reactive"],
            "comment": "Total Reactive Power Present Demand",
        },
        ("kVA_present_demand", ElectricApparentPower): {
            "unit": UNIT["KiloV-A"],
            "comment": "Total Apparent Power Present Demand",
        },
        ("kW_max_demand", ElectricPower): {
            "unit": UNIT["KiloW"],
            "comment": "Total Real Power Maximum Demand",
        },
        ("kVAR_max_demand", ElectricReactivePower): {
            "unit": UNIT["KiloV-A_Reactive"],
            "comment": "Total Reactive Power Maximum Demand",
        },
        ("kVA_max_demand", ElectricApparentPower): {
            "unit": UNIT["KiloV-A"],
            "comment": "Total Apparent Power Maximum Demand",
        },
        ("kWh_A", ElectricEnergy): {
            "unit": UNIT["KiloW-HR"],
            "comment": "Real Energy Consumption Phase A",
        },
        ("kWh_B", ElectricEnergy): {
            "unit": UNIT["KiloW-HR"],
            "comment": "Real Energy Consumption Phase B",
        },
        ("kWh_C", ElectricEnergy): {
            "unit": UNIT["KiloW-HR"],
            "comment": "Real Energy Consumption Phase C",
        },
        ("max_power", ElectricPower): {
            "unit": UNIT["KiloW"],
            "comment": "Maximum Power of device",
        },
    },
    "sensors": {
        ("VoltageAB", VoltageSensor): {
            "comment": "Voltage reading A-B",
            "ofMedium": Electricity,
        },
        ("VoltageAC", VoltageSensor): {
            "comment": "Voltage reading A-C",
            "ofMedium": Electricity,
        },
        ("VoltageBC", VoltageSensor): {
            "comment": "Voltage reading B-C",
            "ofMedium": Electricity,
        },
        ("VoltageAN", VoltageSensor): {
            "comment": "Voltage reading A-N",
            "ofMedium": Electricity,
        },
        ("VoltageBN", VoltageSensor): {
            "comment": "Voltage reading B-N",
            "ofMedium": Electricity,
        },
        ("VoltageCN", VoltageSensor): {
            "comment": "Voltage reading C-N",
            "ofMedium": Electricity,
        },
        ("CurrentPhaseA", CurrentAnalogSensor): {
            "comment": "Current reading of phase A",
            "ofMedium": Electricity,
        },
        ("CurrentPhaseB", CurrentAnalogSensor): {
            "comment": "Current reading of phase B",
            "ofMedium": Electricity,
        },
        ("CurrentPhaseC", CurrentAnalogSensor): {
            "comment": "Current reading of phase C",
            "ofMedium": Electricity,
        },
    },
}


class ThreePhaseElectricalMeter(Device):
    """
    This is an attemp to model a complete Electrical meter
    starting with all the voltages and current sensors.
    All other information being results
    of calculation based on those measures.

    To create one, you must specify a medium and a label
    Sensors will be added to the Meter device and be available
    by square bracket requests.

    """

    _class_iri: URIRef = P223.ElectricalMeter

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(three_phase_electricalmeter_template, config)
        if "medium" not in kwargs:
            raise ValueError(
                "You must provide medium when defining an electrical meter"
            )
        _medium = kwargs.pop("medium")
        for k, v in _config["sensors"].items():
            v["ofMedium"] = _medium

        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)

    def set_measurement_location(self, node: Node = None):
        self.set_voltage_measurement_location(node)
        self.set_current_measurement_location(node)

    def set_voltage_measurement_location(self, node: Node = None):
        for each in self._sensors:
            if isinstance(each, VoltageSensor):
                each.hasMeasurementLocation = node

    def set_current_measurement_location(self, node: Node = None):
        for each in self._sensors:
            if isinstance(each, CurrentAnalogSensor):
                each.hasMeasurementLocation = node
