from pathlib import Path

import hvac_devices as hd
import hvac_spaces as hs

from bob.core import BOB, UNIT, bind_model_namespace, dump
from bob.functions import Function, FunctionInput, FunctionOutput
from bob.producer.occupancy import OccupancyFunction
from bob.properties import Temperature
from bob.properties.states import OccupancyStatus, Schedule
from bob.sensor.temperature import TemperatureSensor

# import lighting_devices as ld
# import lighting_spaces as ls


model_name = Path(__file__).stem
global_ns = Path(__file__).parent.stem
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}/{model_name}/")


#
#   Temperature control
#
# g36_4-1_VAV_TerminalUnit_CoolingOnly
class TempControl(Function):
    _class_iri = BOB.TempControl
    # From table in section 4.1
    # Defined as Function Input and Output as we will connect
    # to existing properties in the model
    zoneSetpoint: FunctionInput
    zoneTemp: FunctionInput
    heatingCommand: FunctionOutput


temp_control = TempControl(label="Zone 1 Temperature Control")
