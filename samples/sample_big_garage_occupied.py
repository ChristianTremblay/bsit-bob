"""
Simple garage with one physical space
Two (2) lighting spaces
In each ligth space there is a movement detector for each set of ligth
"""
from pathlib import Path

from bob.core import (
    s223,
    bind_model_namespace,
    System,
    SystemConnectionPoint,
    dump,
)
from bob.connections.air import (
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.light import LightingSpace
from bob.space.physical import Building, Roof, Floor, Office

from bob.devices.lighting.light import Luminaire
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.coil import ElectricalHeatingCoil
from bob.connections.electricity import ElectricalInletConnectionPoint

from bob.sensor.movement import MovementSensor
from bob.sensor.temperature import AirTemperatureSensor
from header import sample_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


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

movement_1 = MovementSensor(label="Movement Sensor Space #1")
movement_2 = MovementSensor(label="Movement Sensor Space #2")

# HVAC
fan = Fan(label="Fan", electricalInlet=ElectricalInletConnectionPoint)
heating_coil = ElectricalHeatingCoil(label="Heating Coil")

garage_hvac.ductAirOutlet >> fan.airInlet
fan.airOutlet >> heating_coil.airInlet
heating_coil.airOutlet >> garage_hvac.ductAirInlet

dat = AirTemperatureSensor(label="Discharge Air temperature sensor")
znt = AirTemperatureSensor(label="Zone Air temperature sensor")

dat.hasMeasurementLocation = heating_coil.airOutlet
znt.hasMeasurementLocation = garage_hvac
dat.hasPhysicalLocation = big_garage
znt.hasPhysicalLocation = big_garage

# LIGHTS
light_1.lightOutlet >> lighting_space_entry.lightInlet
light_2.lightOutlet >> lighting_space_back.lightInlet
movement_1.hasMeasurementLocation = lighting_space_entry
movement_2.hasMeasurementLocation = lighting_space_back
movement_1.hasPhysicalLocation = big_garage
movement_2.hasPhysicalLocation = big_garage

# SYSTEM
fancoil = System(label="Fan coil")
fc_airInlet = AirInletSystemConnectionPoint(fancoil, label="Fan coil air inlet")
fc_airOutlet = AirOutletSystemConnectionPoint(fancoil, label="Fan coil air outlet")
fc_occupancy = SystemConnectionPoint(
    fancoil, label="Occupancy Inlet", hasDirection=s223["Direction-Inlet"]
)
fc_occupancy.mapsTo = movement_1
fc_airInlet.mapsTo = fan.airInlet
fc_airOutlet.mapsTo = heating_coil.airOutlet

dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
