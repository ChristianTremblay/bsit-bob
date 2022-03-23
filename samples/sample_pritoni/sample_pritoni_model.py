from pathlib import Path

from typing import Any

from bob.connections.light import LightVisibleConnection
from bob.connections.occupancy import (
    OccupancyInletSystemConnectionPoint,
    OccupancyOutletSystemConnectionPoint,
)

from bob.core import p223, get_datagraph, bind_model_namespace, dump, quantitykind, unit

from bob.devices.hvac.damper import ElectricalActuatedDamper
from bob.devices.hvac.coil import ChilledWaterCoil, HotWaterCoil
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.filter import Filter
from bob.devices.hvac.damper import Window
from bob.devices.lighting.light import Luminaire

from bob.devices.electricity.distribution import (
    DistributionPanel,
    Transformer,
    SinglePhaseDistributionPanel,
    SinglePoleCircuitBreaker,
    ThreePhasesDistributionPanel,
    ThreePolesCircuitBreaker,
    ThreePolesMainCircuitBreaker,
    TwoPolesCircuitBreaker,
    TwoPolesMainCircuitBreaker,
)
from bob.property import QuantifiableObservableProperty

from bob.space.occupancy import OccupancySpace
from bob.systems.hvac.airhandlingunit import AirHandlingUnit
from bob.systems.hvac.vav import VAV
from bob.sensor.temperature import AirTemperatureSensor
from bob.sensor.flow import AirFlowSensor
from bob.sensor.movement import MovementSensor, OccupancySensor

from bob.space.physical import Building, Floor, Roof, Office, Room, Bathroom, Corridor
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.light import LightingSpace, LightingZone

from bob.systems.functionblock import FunctionBlock

from bob.connections.air import *
from bob.connections.electricity import *

from header import sample_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")

import physical_spaces as ps
import hvac_spaces as hs
import occupancy_spaces as os
import lighting_spaces as ls

import hvac_devices as hd
import lighting_devices as ld
import electrical_devices as ed

import hvac
import lighting
import electricity
import occupancy
import bacnet_references

# Relations between Physical spaces and Domain spaces
ps.bldg > ps.roof
ps.bldg > ps.floor1
ps.floor1 > ps.openoffice > hs.openoffice_hvac
ps.openoffice > ls.openofficeEast_lightspace
ps.openoffice > ls.openofficeWest_lightspace
ps.openoffice > os.openoffice_occ_space

ps.floor1 > ps.bathroom > hs.bathroom_hvac
ps.bathroom > ls.bathroom_lightspace

ps.floor1 > ps.corridor > hs.corridorNorth_hvac
ps.corridor > hs.corridorSouth_hvac
ps.corridor > ls.corridor_lightspace

ps.floor1 > ps.private_office > hs.privateoffice_hvac
ps.private_office > ls.privateoffice_lightspace

ps.floor1 > ps.kitchenette > hs.kitchenette_hvac
ps.kitchenette > ls.kitchenette_lightspace
ps.kitchenette > os.kitchenette_occ_space

dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
