from pathlib import Path
from typing import Any

from header import sample_header

from bob.connections.air import *
from bob.connections.electricity import *
from bob.connections.light import LightVisibleConnection
from bob.core import bind_model_namespace, dump, data_graph, schema_graph
from bob.devices.architectural import Window
from bob.devices.hvac.coil import ChilledWaterCoil, HotWaterCoil
from bob.devices.hvac.damper import ElectricalActuatedProportionalDamper
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.filter import Filter
from bob.devices.lighting.light import Luminaire
from bob.property import QuantifiableObservableProperty
from bob.sensor.flow import AirFlowSensor
from bob.sensor.light import MovementSensor, OccupancySensor
from bob.sensor.temperature import AirTemperatureSensor
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.light import LightingSpace, LightingZone
from bob.space.physical import Bathroom, Building, Corridor, Floor, Office, Roof, Room
from bob.systems.hvac.airhandlingunit import AirHandlingUnit
from bob.systems.hvac.vav import VAV

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")

import physical_spaces as ps  # isort: skip
import hvac_devices as hd  # isort: skip
import hvac_spaces as hs  # isort: skip
import hvac  # isort: skip
import lighting_spaces as ls  # isort: skip
import lighting_devices as ld  # isort: skip
import lighting  # isort: skip
import network_devices as nd  # isort: skip
import electrical_devices as ed  # isort: skip
import electricity  # isort: skip

import functions  # isort: skip
import bacnet_references  # isort: skip
import fake_values  # isort: skip

# Relations between Physical spaces and Domain spaces
ps.bldg > ps.roof
ps.bldg > ps.floor1
ps.floor1 > ps.openoffice > hs.openoffice_hvac
ps.openoffice > ls.openofficeEast_lightspace
ps.openoffice > ls.openofficeWest_lightspace

ps.floor1 > ps.bathroom > hs.bathroom_hvac
ps.bathroom > ls.bathroom_lightspace

ps.floor1 > ps.corridor > hs.corridorNorth_hvac
ps.corridor > hs.corridorSouth_hvac
ps.corridor > ls.corridor_lightspace

ps.floor1 > ps.private_office > hs.privateoffice_hvac
ps.private_office > ls.privateoffice_lightspace

ps.floor1 > ps.kitchenette > hs.kitchenette_hvac
ps.kitchenette > ls.kitchenette_lightspace

dump(data_graph, filename=f"samples/ttl/{model_name}.data.ttl", header=sample_header(model_name))
dump(schema_graph, filename=f"samples/ttl/{model_name}.schema.ttl", header=sample_header(model_name))
