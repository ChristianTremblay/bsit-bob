from pathlib import Path

import electrical_devices as ed
import hvac_devices as hd
import lighting_devices as ld
import physical_spaces as ps

from bob.connections.electricity import *
from bob.core import bind_model_namespace, dump
from bob.devices.network.switch import EthernetSwitch

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")

ethernet_switch = EthernetSwitch(label="Simple Switch", ports=8, data_rate=1000)

ethernet_switch.port0 >> hd.ahu["RF-VFD"].ethernet_port
