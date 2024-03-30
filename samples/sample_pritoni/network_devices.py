from pathlib import Path

import electrical_devices as ed
import hvac_devices as hd
import lighting_devices as ld
import physical_spaces as ps

from bob.core import bind_model_namespace, dump
from bob.equipment.network.firewall import EthernetFirewall, internet
from bob.equipment.network.switch import EthernetSwitch

model_name = Path(__file__).stem
global_ns = Path(__file__).parent.stem
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}/{model_name}/")

ethernet_switch = EthernetSwitch(label="Simple Switch", ports=8, data_rate=1000)

ethernet_switch.port1 >> hd.ahu["RF_VFD"].ethernet_port

firewall = EthernetFirewall(label="Firewall", wan_ports=1, lan_ports=4, data_rate=1000)

internet >> firewall.wan_port0
firewall.lan_port0 >> ethernet_switch.port0
