from pathlib import Path
from typing import Any

from bob.assemblage import create_data_and_schema_ttl
from bob.connections.air import *
from bob.connections.liquid import (
    WaterConnection,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from bob.core import (
    P223,
    UNIT,
    Equipment,
    System,
    bind_model_namespace,
    dump,
    get_datagraph,
)
from bob.equipment.architectural import Window
from bob.equipment.hvac.airhandlingunit import AirHandlingUnit
from bob.equipment.hvac.boiler import ElectricalHotWaterBoiler, HotWaterBoiler
from bob.equipment.hvac.coil import ChilledWaterCoil, HotWaterCoil
from bob.equipment.hvac.damper import ElectricalActuatedDamper
from bob.equipment.hvac.fan import Fan
from bob.equipment.hvac.filter import Filter
from bob.equipment.hvac.pump import Pump
from bob.equipment.hvac.valve import TwoWayValve
from bob.equipment.hvac.vav import VAV
from bob.equipment.lighting.light import Luminaire
from bob.scratch.header import sample_header
from bob.sensor.flow import AirFlowSensor
from bob.sensor.temperature import AirTemperatureSensor
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.light import LightingSpace, LightingZone
from bob.space.physical import Bathroom, Building, Corridor, Floor, Office, Roof, Room

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def sample_using_only_water_medium():
    class AgnosticWaterBoiler(Equipment):
        node_type = P223.AgnosticBoiler
        waterInlet: WaterInletConnectionPoint
        waterOutlet: WaterOutletConnectionPoint

    class AgnosticWaterCoil(Equipment):
        node_type = P223.AgnosticCoil
        waterInlet: WaterInletConnectionPoint
        waterOutlet: WaterOutletConnectionPoint

    class HotWaterTank(Equipment):
        node_type = P223.HotWaterTank
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
    DHWSystem > [
        DHWBoiler,
        dhw_hot_water_tank,
    ]  ###TODO: dhw_supply_for_house must be a Equipment or system


if __name__ == "__main__":
    r = sample_using_only_water_medium()
    _folder = Path(__file__).parent
    create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))

    graph = get_datagraph()
