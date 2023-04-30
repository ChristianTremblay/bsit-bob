from typing import Dict

from bob.enum import Dimensioned, ElectricalPhaseIdentifier
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
from bob.sensor.electricity import CurrentSensor, VoltageSensor

from ...connections.electricity import *
from ...core import BOB, P223, S223, UNIT, Equipment, Node, template_update

_namespace = BOB

three_phase_electricalmeter_template = {
    "properties": {
        ("energy", ElectricEnergy): {
            "unit": UNIT["KiloW-HR"],
            "comment": "Real Energy Consumption",
            "hasAspect": ElectricalPhaseIdentifier.ABC,
        },
        ("kW_total", ElectricPower): {
            "unit": UNIT["KiloW"],
            "comment": "Total Real Power",
            "hasAspect": ElectricalPhaseIdentifier.ABC,
        },
        ("kVAR_total", ElectricReactivePower): {
            "unit": UNIT["KiloV-A_Reactive"],
            "comment": "Total Reactive Power",
            "hasAspect": ElectricalPhaseIdentifier.ABC,
        },
        ("kVA_total", ElectricApparentPower): {
            "unit": UNIT["KiloV-A"],
            "comment": "Total Apparent Power",
            "hasAspect": ElectricalPhaseIdentifier.ABC,
        },
        ("power_factor", PowerFactor): {"comment": "Total Power Factor"},
        ("voltage_ll_avg", Volts): {
            "comment": "Voltage L-L Average",
            "hasAspect": [ElectricalPhaseIdentifier.ABC, Dimensioned.LineLineVoltage],
        },
        ("voltage_ln_avg", Volts): {
            "comment": "Voltage L-N Average",
            "hasAspect": [
                ElectricalPhaseIdentifier.ABC,
                Dimensioned.LineNeutralVoltage,
            ],
        },
        ("current_avg", Volts): {
            "comment": "Current Average",
            "hasAspect": ElectricalPhaseIdentifier.ABC,
        },
        ("kW_A", ElectricPower): {
            "unit": UNIT["KiloW"],
            "comment": "Real Power Phase A",
            "hasAspect": ElectricalPhaseIdentifier.A,
        },
        ("kW_B", ElectricPower): {
            "unit": UNIT["KiloW"],
            "comment": "Real Power Phase B",
            "hasAspect": ElectricalPhaseIdentifier.B,
        },
        ("kW_C", ElectricPower): {
            "unit": UNIT["KiloW"],
            "comment": "Real Power Phase C",
            "hasAspect": ElectricalPhaseIdentifier.C,
        },
        ("power_factor_A", PowerFactor): {
            "comment": "Power Factor Phase A",
            "hasAspect": ElectricalPhaseIdentifier.A,
        },
        ("power_factor_B", PowerFactor): {
            "comment": "Power Factor Phase B",
            "hasAspect": ElectricalPhaseIdentifier.B,
        },
        ("power_factor_C", PowerFactor): {
            "comment": "Power Factor Phase C",
            "hasAspect": ElectricalPhaseIdentifier.C,
        },
        ("frequency", Frequency): {
            "comment": "Frequency",
            "hasAspect": Dimensioned.NominalFrequency,
        },
        ("kVAh", ElectricApparentEnergy): {
            "unit": UNIT["KiloV-A-HR"],
            "comment": "Apparent Energy Consumption",
            "hasAspect": ElectricalPhaseIdentifier.ABC,
        },
        ("kVARh", ElectricReactiveEnergy): {
            "unit": UNIT["KiloV-A_Reactive-HR"],
            "comment": "Reactive Energy Consumption",
            "hasAspect": ElectricalPhaseIdentifier.ABC,
        },
        ("kVA_A", ElectricApparentPower): {
            "unit": UNIT["KiloV-A"],
            "comment": "Apparent Power Phase A",
            "hasAspect": ElectricalPhaseIdentifier.A,
        },
        ("kVA_B", ElectricApparentPower): {
            "unit": UNIT["KiloV-A"],
            "comment": "Apparent Power Phase B",
            "hasAspect": ElectricalPhaseIdentifier.B,
        },
        ("kVA_C", ElectricApparentPower): {
            "unit": UNIT["KiloV-A"],
            "comment": "Apparent Power Phase C",
            "hasAspect": ElectricalPhaseIdentifier.C,
        },
        ("kVAR_A", ElectricReactivePower): {
            "unit": UNIT["KiloV-A_Reactive"],
            "comment": "Reactive Power Phase A",
            "hasAspect": ElectricalPhaseIdentifier.A,
        },
        ("kVAR_B", ElectricReactivePower): {
            "unit": UNIT["KiloV-A_Reactive"],
            "comment": "Reactive Power Phase B",
            "hasAspect": ElectricalPhaseIdentifier.B,
        },
        ("kVAR_C", ElectricReactivePower): {
            "unit": UNIT["KiloV-A_Reactive"],
            "comment": "Reactive Power Phase C",
            "hasAspect": ElectricalPhaseIdentifier.C,
        },
        ("kW_present_demand", ElectricPower): {
            "unit": UNIT["KiloW"],
            "comment": "Total Real Power Present Demand",
            "hasAspect": ElectricalPhaseIdentifier.ABC,
        },
        ("kVAR_present_demand", ElectricReactivePower): {
            "unit": UNIT["KiloV-A_Reactive"],
            "comment": "Total Reactive Power Present Demand",
            "hasAspect": ElectricalPhaseIdentifier.ABC,
        },
        ("kVA_present_demand", ElectricApparentPower): {
            "unit": UNIT["KiloV-A"],
            "comment": "Total Apparent Power Present Demand",
            "hasAspect": ElectricalPhaseIdentifier.ABC,
        },
        ("kW_max_demand", ElectricPower): {
            "unit": UNIT["KiloW"],
            "comment": "Total Real Power Maximum Demand",
            "hasAspect": ElectricalPhaseIdentifier.ABC,
        },
        ("kVAR_max_demand", ElectricReactivePower): {
            "unit": UNIT["KiloV-A_Reactive"],
            "comment": "Total Reactive Power Maximum Demand",
            "hasAspect": ElectricalPhaseIdentifier.ABC,
        },
        ("kVA_max_demand", ElectricApparentPower): {
            "unit": UNIT["KiloV-A"],
            "comment": "Total Apparent Power Maximum Demand",
            "hasAspect": ElectricalPhaseIdentifier.ABC,
        },
        ("kWh_A", ElectricEnergy): {
            "unit": UNIT["KiloW-HR"],
            "comment": "Real Energy Consumption Phase A",
            "hasAspect": ElectricalPhaseIdentifier.A,
        },
        ("kWh_B", ElectricEnergy): {
            "unit": UNIT["KiloW-HR"],
            "comment": "Real Energy Consumption Phase B",
            "hasAspect": ElectricalPhaseIdentifier.B,
        },
        ("kWh_C", ElectricEnergy): {
            "unit": UNIT["KiloW-HR"],
            "comment": "Real Energy Consumption Phase C",
            "hasAspect": ElectricalPhaseIdentifier.C,
        },
        ("max_power", ElectricPower): {
            "unit": UNIT["KiloW"],
            "comment": "Maximum Power of Equipment",
            "hasAspect": ElectricalPhaseIdentifier.ABC,
        },
    },
    "sensors": {
        ("VoltageAB", VoltageSensor): {
            "comment": "Voltage reading A-B",
            # "ofMedium": Electricity,
            "hasAspect": ElectricalPhaseIdentifier.AB,
        },
        ("VoltageAC", VoltageSensor): {
            "comment": "Voltage reading C-A",
            # "ofMedium": Electricity,
            "hasAspect": ElectricalPhaseIdentifier.CA,
        },
        ("VoltageBC", VoltageSensor): {
            "comment": "Voltage reading B-C",
            # "ofMedium": Electricity,
            "hasAspect": ElectricalPhaseIdentifier.BC,
        },
        ("VoltageAN", VoltageSensor): {
            "comment": "Voltage reading A-N",
            # "ofMedium": Electricity,
            "hasAspect": ElectricalPhaseIdentifier.A,
        },
        ("VoltageBN", VoltageSensor): {
            "comment": "Voltage reading B-N",
            # "ofMedium": Electricity,
            "hasAspect": ElectricalPhaseIdentifier.B,
        },
        ("VoltageCN", VoltageSensor): {
            "comment": "Voltage reading C-N",
            # "ofMedium": Electricity,
            "hasAspect": ElectricalPhaseIdentifier.C,
        },
        ("CurrentPhaseA", CurrentSensor): {
            "comment": "Current reading of phase A",
            # "ofMedium": Electricity,
            "hasAspect": ElectricalPhaseIdentifier.A,
        },
        ("CurrentPhaseB", CurrentSensor): {
            "comment": "Current reading of phase B",
            # "ofMedium": Electricity,
            "hasAspect": ElectricalPhaseIdentifier.B,
        },
        ("CurrentPhaseC", CurrentSensor): {
            "comment": "Current reading of phase C",
            # "ofMedium": Electricity,
            "hasAspect": ElectricalPhaseIdentifier.C,
        },
    },
}


class ThreePhaseElectricalMeter(Equipment):
    """
    This is an attemp to model a complete Electrical meter
    starting with all the voltages and current sensors.
    All other information being results
    of calculation based on those measures.

    To create one, you must specify a medium and a label
    Sensors will be added to the Meter Equipment and be available
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
                each % node

    def set_current_measurement_location(self, node: Node = None):
        for each in self._sensors:
            if isinstance(each, CurrentSensor):
                each % node
