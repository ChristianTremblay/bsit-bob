from pathlib import Path

import hvac_devices as hd

from bob.core import FunctionBlock, bind_model_namespace
from bob.properties import Temperature
from bob.sensor.temperature import TemperatureSensor

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace(model_name, f"urn:ex/{model_name}/")


class AVG_Temp(FunctionBlock):
    avg_tmp: Temperature


f = AVG_Temp(label="FB-1", comment="Compute DA-T Avg", avg_tmp=0)

f.uses_input(hd.ahu["DA-T"].observesProperty)
f.produces_output(f.avg_tmp)
