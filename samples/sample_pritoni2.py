from pathlib import Path
from bob.core import (
    bind_model_namespace,
    PhysicalSpace,
    DomainSpace,
    Domain,
    HVAC,
    Lighting,
    Medium,
    Air,
    Light,
    dump,
)
from bob.sensor import Sensor

from bob.space.hvac import HVACZone
from bob.space.physical import Room, Office, Bathroom, Corridor
from bob.devices.hvac.fan import Fan
from bob.systems.hvac.vav import VAV1
from header import sample_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", "ex:pritoni2:")


class PrivateOffice(Office):
    pass


class Kitchenette(Room):
    pass


class LightingSpace(DomainSpace):
    hasDomain: Domain = Lighting
    hasMedium: Medium = Light


class HVACSpace(DomainSpace):
    hasDomain: Domain = HVAC
    hasMedium: Medium = Air


open_office = Office(label="OpenOffice")
lz1 = LightingSpace(label="LZ1")
lz2 = LightingSpace(label="LZ2")
open_office_hvac = HVACSpace(label="OpenOffice.HVAC")
open_office > lz1
open_office > lz2
open_office > open_office_hvac

bathroom = Bathroom(label="Bathroom")
lz3 = LightingSpace(label="LZ3")
bathroom_hvac = HVACSpace(label="Bathroom.HVAC")
bathroom > lz3
bathroom_exhaust_fan = Fan(label="Bathroom.ExhaustFan")

corridor = Corridor(label="Corridor")
lz4 = LightingSpace(label="LZ4")
corridor_hvac = HVACSpace(label="Corridor.HVAC")
corridor > lz4

private_office = PrivateOffice(label="PrivateOffice")
lz5 = LightingSpace(label="LZ5")
private_office_hvac = HVACSpace(label="PrivateOffice.HVAC")
private_office > lz5

kitchenette = Kitchenette(label="Kitchenette")
lz6 = LightingSpace(label="LZ6")
kitchenette_hvac = HVACSpace(label="Kitchenette.HVAC")
kitchenette > lz6

hvac_zone_1 = HVACZone(label="HVACZone1")
hvac_zone_2 = HVACZone(label="HVACZone2")

vav1 = VAV1(label="VAV1")
vav2 = VAV1(label="VAV2")

dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
