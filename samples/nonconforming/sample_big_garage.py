"""
Simple garage with one physical space
Two (2) lighting spaces
In each lighting space there is a movement detector for each set of lights
"""

from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.connections.electricity import ElectricalInletConnectionPoint
from bob.core import UNIT, bind_model_namespace, dump
from bob.equipment.hvac.coil import ElectricalHeatingCoil
from bob.equipment.hvac.fan import Fan
from bob.equipment.lighting.light import Luminaire
from bob.scratch.header import sample_header
from bob.sensor.motion import OccupantMotionSensor
from bob.sensor.temperature import AirTemperatureSensor
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.light import LightingSpace
from bob.space.physical import Building, Floor, Office, Roof

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


big_garage = Building(label="My Building")
roof = Roof(label="Roof of building")

garage_hvac = HVACSpace(label="My Big Garage")
lighting_space_entry = LightingSpace(label="Light Space #1 near entry")
lighting_space_back = LightingSpace(label="Light Space #2 back of the garage")

# Physical relationships
big_garage > roof
big_garage > garage_hvac
big_garage > lighting_space_entry
big_garage > lighting_space_back

light_1 = Luminaire(label="Ballast #1, space #1")
light_2 = Luminaire(label="Ballast #2, space #2")

movement_1 = OccupantMotionSensor(label="Movement Sensor Space #1")
movement_2 = OccupantMotionSensor(label="Movement Sensor Space #2")

# HVAC
fan = Fan(label="Fan", electricalInlet=ElectricalInletConnectionPoint)
heating_coil = ElectricalHeatingCoil(label="Heating Coil")

garage_hvac.ductAirOutlet >> fan.airInlet
fan.airOutlet >> heating_coil.airInlet
heating_coil.airOutlet >> garage_hvac.ductAirInlet

dat = AirTemperatureSensor(label="Discharge Air temperature sensor", hasUnit=UNIT.DEG_C)
znt = AirTemperatureSensor(label="Zone Air temperature sensor", hasUnit=UNIT.DEG_C)

dat % heating_coil.airOutlet
znt % garage_hvac
dat.hasPhysicalLocation = big_garage
znt.hasPhysicalLocation = big_garage

# LIGHTS
light_1.lightOutlet >> lighting_space_entry.lightInlet
light_2.lightOutlet >> lighting_space_back.lightInlet
movement_1 % lighting_space_entry
movement_2 % lighting_space_back
movement_1.hasPhysicalLocation = big_garage
movement_2.hasPhysicalLocation = big_garage

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
