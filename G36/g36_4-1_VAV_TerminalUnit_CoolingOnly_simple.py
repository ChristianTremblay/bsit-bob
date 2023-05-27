"""
g36_4-1_VAV_TerminalUnit_CoolingOnly
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from header import g36_header

from bob.connections.air import (
    AirConnection,
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from bob.connections.electricity import (
    Electricity_24V_1Ph_60HzInletConnectionPoint,
)
from bob.connections.network import (
    RS485BidirectionalConnectionPoint,
)
from bob.core import (
    G36,
    QUANTITYKIND,
    UNIT,
    Equipment,
    PropertyReference,
    System,
    bind_model_namespace,
    dump,
)
from bob.enum import AnalogSignalTypeEnum
from bob.equipment.architectural import Window
from bob.equipment.control import AnalogInput, AnalogOutput, BinaryInput, BinaryOutput
from bob.equipment.control.controller import Controller
from bob.equipment.hvac.damper import ElectricalActuatedProportionalDamper
from bob.equipment.hvac.gas import GasMonitor
from bob.equipment.hvac.stats import NetworkRoomSensor, NetworkThermostat
from bob.producer import (
    FunctionBlock,
    G36AnalogInput,
    G36AnalogOutput,
    G36BinaryInput,
    G36BinaryOutput,
)
from bob.producer.g36 import VAV_CoolingOnly_template, G36VAVCoolingOnly
from bob.producer.occupancy import OccupancyFunction
from bob.properties import Flow, PercentCommand, Temperature, temperature
from bob.properties.states import OccupancyStatus
from bob.properties.ratio import Percent
from bob.property import QuantifiableObservableProperty
from bob.sensor.flow import AirFlowSensor
from bob.sensor.gas import CO2Sensor
from bob.sensor.motion import OccupantMotionSensor
from bob.sensor.security import IntrusionSensor
from bob.sensor.temperature import AirTemperatureSensor, TemperatureSetpoint
from bob.space.hvac import HVACSpace, HVACZone

model_name = Path(__file__).stem
_namespace = bind_model_namespace(
    "exg3601", f"http://data.ashrae.org/standard223/data/{model_name}#"
)

g36VAVcoolingOnly = G36VAVCoolingOnly(label="Simplest implementation")
dump(filename=f"G36/ttl/{model_name}.ttl", header=g36_header(model_name))
