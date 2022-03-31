from pathlib import Path

from typing import Any

from bob.core import (
    p223,
    Device,
    System,
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
from bob.devices.hvac.valve import TwoWayValve
from bob.devices.lighting.light import Luminaire
from bob.systems.hvac.airhandlingunit import AirHandlingUnit
from bob.systems.hvac.vav import VAV
from bob.devices.hvac.pump import Pump
from bob.sensor.temperature import AirTemperatureSensor
from bob.sensor.flow import AirFlowSensor
from bob.sensor.movement import MovementSensor

from bob.space.physical import Building, Floor, Roof, Office, Room, Bathroom, Corridor
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.light import LightingSpace, LightingZone

from bob.connections.air import *
from bob.connections.water import (
    WaterConnection,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)

from header import sample_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def sample_using_only_water_medium():
    class AgnosticWaterBoiler(Device):
        node_type = p223.AgnosticBoiler
        waterInlet: WaterInletConnectionPoint
        waterOutlet: WaterOutletConnectionPoint

    class AgnosticWaterCoil(Device):
        node_type = p223.AgnosticCoil
        waterInlet: WaterInletConnectionPoint
        waterOutlet: WaterOutletConnectionPoint

    class HotWaterTank(Device):
        node_type = p223.HotWaterTank
        waterInlet: WaterInletConnectionPoint
        waterOutlet: WaterOutletConnectionPoint

    DHWBoiler = AgnosticWaterBoiler(label="DHW-BOILER")
    htgloop_boiler = AgnosticWaterBoiler(label="HTGLOOP-BOILER")
    dhw_hot_water_tank = HotWaterTank(label="DHW-TANK")

    htg_hot_water_tank = HotWaterTank(label="HTG-TANK")

    city_water_tap = WaterConnection(label="CITY-WATER")
    dhw_supply_for_house = WaterConnection(label="HouseFaucets")
    kitchen_faucet = TwoWayValve(label="KITCHENFAUCET")
    house_drain = WaterConnection(label="HOUSE-DRAIN")
    city_drain = WaterConnection(label="CityDrain")

    htg_pump = Pump(label="HowWaterPump")
    house_hw_supply = WaterConnection(label="HotWaterSupply")
    house_hw_return = WaterConnection(label="HotWaterReturn")
    joelsofficeheatingvalve = TwoWayValve(label="joelsofficehtgvlv")
    joelsofficeheatingcoil = AgnosticWaterCoil(label="JoelsOfficeCoil")
    fillingValve = TwoWayValve(
        label="FILL-VLV", comment="Fill Hot Water Loop with water"
    )

    city_water_tap >> DHWBoiler.waterInlet
    DHWBoiler.waterOutlet >> dhw_hot_water_tank.waterInlet
    dhw_hot_water_tank.waterOutlet >> dhw_supply_for_house >> kitchen_faucet.waterInlet
    kitchen_faucet.waterOutlet >> city_drain

    htg_hot_water_tank.waterOutlet >> htgloop_boiler.waterInlet
    htgloop_boiler.waterOutlet >> htg_pump.waterInlet
    htg_pump.waterOutlet >> house_hw_supply >> joelsofficeheatingvalve.waterInlet
    joelsofficeheatingvalve.waterOutlet >> joelsofficeheatingcoil.waterInlet
    joelsofficeheatingcoil.waterOutlet >> house_hw_return
    house_hw_return >> htg_hot_water_tank.waterInlet
    city_water_tap >> fillingValve.waterInlet
    fillingValve.waterOutlet >> house_hw_return

    DHWSystem = System(label="DHW", comment="DHW loop in my house")
    DHWSystem > [DHWBoiler, dhw_hot_water_tank] ###TODO: dhw_supply_for_house must be a device or system


if __name__ == "__main__":
    r = sample_using_only_water_medium()
    result = dump(
        filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name)
    )
    graph = get_datagraph()
