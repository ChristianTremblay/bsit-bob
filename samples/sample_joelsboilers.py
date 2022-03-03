from pathlib import Path

from typing import Any

from matplotlib.backend_bases import MouseEvent

from bob.core import (
    Device,
    get_datagraph,
    bind_model_namespace,
    dump,
)

from bob.devices.hvac.damper import ElectricalActuatedDamper
from bob.devices.hvac.coil import ChilledWaterCoil, HotWaterCoil
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.filter import Filter
from bob.devices.hvac.damper import Window
from bob.devices.hvac.boiler import HotWaterBoiler, ElectricalHotWaterBoiler
from bob.devices.lighting.light import Light
from bob.systems.hvac.airhandlingunit import AirHandlingUnit
from bob.systems.hvac.vav import VAV
from bob.sensor.temperature import AirTemperatureSensor
from bob.sensor.flow import AirFlowSensor
from bob.sensor.movement import MovementSensor

from bob.space.physical import Building, Floor, Roof, Office, Room, Bathroom, Corridor
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.light import LightingSpace, LightingZone

from bob.connections.air import *
from bob.connections.water import WaterConnection, WaterInletConnectionPoint, WaterOutletConnectionPoint

DHWBoiler = ElectricalHotWaterBoiler(label='DHW-BOILER')
htgloop_boiler = HotWaterBoiler(label='HTGLOOP-BOILER')
hot_water_tank = Device(label='DHW-TANK', waterInlet=WaterInletConnectionPoint(), waterOutlet=WaterOutletConnectionPoint())

city_water_tap = WaterConnection(label='CITY-WATER')

