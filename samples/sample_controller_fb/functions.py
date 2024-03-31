from pathlib import Path

import hvac_devices as hd
import bacnet_references as bn
from bob.core import UNIT, bind_model_namespace, dump
from bob.functions import Function, FunctionInput, FunctionOutput
from bob.producer.occupancy import OccupancyFunction
from bob.properties import Temperature, PercentCommand
from bob.properties.states import OccupancyStatus, Schedule, OnOffCommand
from bob.sensor.temperature import TemperatureSensor

model_name = Path(__file__).stem
global_ns = Path(__file__).parent.stem
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}/{model_name}/")


class LessThan(Function):
    """
    y = u1 < u2
    """

    u1: FunctionInput
    u2: FunctionInput
    y: FunctionOutput


# line up the output to a special property
heating_command = PercentCommand(label="vav1_heat_c")
zone_setpoint = Temperature(label="Zone Temp Setpoint", hasValue=21, hasUnit=UNIT.DEG_C)
zone_setpoint @ bn.zone1_temp_sp.presentValue
# make an instance
f = LessThan(
    label="Heatin Command Block",
    comment="Will turn on heating if temp is less than setpoint",
    u1=hd.vav1["ZN-T"].observedProperty,
    u2=zone_setpoint,
    y=heating_command,
)
f.y >> hd.vav1["REHEAT"]["modulation"]
hd.vav1.executes(f)
