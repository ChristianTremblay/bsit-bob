from pathlib import Path

from bob.core import (
    bind_model_namespace,
    dump,
)
from bob.connections.air import (
    AirConnection,
    AirConnectionPoint,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.physical import Building, Roof, Floor, Office
from bob.devices.hvac.coil import ElectricalRadiantHeatingCoil, ElectricalHeatingCoil
from header import sample_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


"""
In this scenario, There are 4 connection points in the HVAC space
but there is no relationship between those connections except that
they are related to the space.
"""
building = Building(label="My Building")
roof = Roof(label="Roof of building")
floor = Floor(label="Floor1")
basement = Floor(label="Basement")
office1 = Office(label="Office 1")
office2 = Office(label="Office 2")
office3 = Office(label="Office 3")
joelsoffice = Office(label="Joel's Office")

office1_hvac = HVACSpace(label="Office 1")
office2_hvac = HVACSpace(label="Office 2")
office3_hvac = HVACSpace(label="Office 3")
basementhvac = HVACSpace(label="Basement HVAC Space")
joelsoffice_hvac = HVACSpace(label="Joel's Office HVAC Space")

zone1 = HVACZone(label="Zone1")

# Physical relationships
building > roof
building > floor
building > basement
floor > office1
floor > office2
floor > office3
basement > joelsoffice > joelsoffice_hvac

# Spaces relationships
# SPACES     | PHYSICAL
office1_hvac < office1
office2_hvac < office2
office3_hvac < office3

basementhvac < basement

# Zones (group of spaces)
# Here, Zone1 contains office1 and office2
office1_hvac < zone1
office2_hvac < zone1

baseboard = ElectricalHeatingCoil(label="Baseboard heater")
# AirInJoelsOfficeSpace = AirConnection(label="Air inside the office")
airFromSpace = AirOutletConnectionPoint(
    joelsoffice_hvac,
    label="Internal Use To be treated",
    comment="Air that doesn't leave the room, used internally by a radiant heater for example",
)
airFromBaseboard = AirInletConnectionPoint(
    joelsoffice_hvac,
    label="Internal Use treated",
    comment="Air that doesn't leave the room, used internally",
)

airFromBaseboard << baseboard
airFromSpace >> baseboard

dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
