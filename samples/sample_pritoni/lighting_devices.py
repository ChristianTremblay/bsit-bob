from pathlib import Path
from bob.devices.electricity.switch import DimmableSwitch

import lighting_spaces as ls
import physical_spaces as ps

from bob.connections.light import *
from bob.core import bind_model_namespace, dump, UNIT
from bob.devices.electricity.switch import DimmableSwitch
from bob.devices.lighting.light import *
from bob.externalreference.bacnet import BACnetReference
from bob.properties.electricity import ElectricPower
from bob.properties.light import RelativeLuminousFlux
from bob.properties.states import OnOffCommand
from bob.sensor.light import DaylightSensor, MovementSensor, OccupancySensor

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")


# Now we build lights for Kitchenette
kitchenette_luminaire_11 = Luminaire(
    label="Luminaire11",
    comment="Luminaire in kitchenette #11",
    hasPhysicalLocation=ps.kitchenette,
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=ElectricPower(100, unit=UNIT.W),
    onOffStatus=OnOffStatus(),
    onOffCommand=OnOffCommand(),
)
kitchenette_luminaire_12 = Luminaire(
    label="Luminaire12",
    comment="Luminaire in kitchenette #12",
    hasPhysicalLocation=ps.kitchenette,
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=ElectricPower(100, unit=UNIT.W),
    onOffStatus=OnOffStatus(),
    onOffCommand=OnOffCommand(),
)
kitchenette_movement = OccupancySensor(
    label="OccSensor4",
    comment="Occupancy sensor for kitchenette luminaires 11 & 12 (O4)",
)
kitch_light_conn = LightVisibleConnection(
    label="LightHub_11_12", comment="Needed to connect multiple luminaires to space"
)


# Now we build lights for Private Office
privateoffice_luminaire_7 = Luminaire(
    label="Luminaire7",
    comment="Luminaire #7 in Private Office",
    hasPhysicalLocation=ps.private_office,
    onOffStatus=OnOffStatus(),
    onOffCommand=OnOffCommand(),
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=ElectricPower(60, unit=UNIT.W),
)
privateoffice_luminaire_8 = Luminaire(
    label="Luminaire8",
    comment="Luminaire #8 in Private Office",
    hasPhysicalLocation=ps.private_office,
    onOffStatus=OnOffStatus(),
    onOffCommand=OnOffCommand(),
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=ElectricPower(60, unit=UNIT.W),
)
privateoffice_movement = MovementSensor(
    label="OccSensor3",
    comment="Occupancy sensor for Privtae Office (O3)",
    hasPhysicalLocation=ps.private_office,
    hasMeasurementLocation=ls.privateoffice_lightspace,
)
privateoffice_light_conn = LightVisibleConnection(
    label="LightHub_7_8", comment="Needed to connect multiple luminaires to space"
)


# privateoffice_movement.hasMeasurementLocation = privateoffice_lightspace
# privateoffice_movement.hasPhysicalLocation = private_office

# Now we build lights for Corridor
corridor_luminaire_9 = Luminaire(
    label="Luminaire9",
    comment="Luminaire #9 in Corridor",
    hasPhysicalLocation=ps.corridor,
    onOffStatus=OnOffStatus(),
    onOffCommand=OnOffCommand(),
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=ElectricPower(100, unit=UNIT.W),
)
corridor_luminaire_10 = Luminaire(
    label="Luminaire10",
    comment="Luminaire #10 in Corridor",
    hasPhysicalLocation=ps.corridor,
    onOffStatus=OnOffStatus(),
    onOffCommand=OnOffCommand(),
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=ElectricPower(100, unit=UNIT.W),
)
corridor_movement = OccupancySensor(
    label="OccSensor5",
    comment="Occupancy sensor for Corridor (O5)",
)
corridor_light_conn = LightVisibleConnection(
    label="LightHub_9_10", comment="Needed to connect multiple luminaires to space"
)


# Now we build lights for Bathroom
bathroom_luminaire_5 = Luminaire(
    label="Luminaire5",
    comment="Luminaire #5 in Bathroom",
    hasPhysicalLocation=ps.bathroom,
    onOffStatus=OnOffStatus(),
    onOffCommand=OnOffCommand(),
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=ElectricPower(60, unit=UNIT.W),
)
bathroom_luminaire_6 = Luminaire(
    label="Luminaire6",
    comment="Luminaire #6 in Bathroom",
    hasPhysicalLocation=ps.bathroom,
    onOffStatus=OnOffStatus(),
    onOffCommand=OnOffCommand(),
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=ElectricPower(60, unit=UNIT.W),
)
bathroom_light_conn = LightVisibleConnection(
    label="LightHub_5_6", comment="Needed to connect multiple luminaires to space"
)
bathroom_movement = OccupancySensor(
    label="OccSensor2",
    comment="Occupancy sensor for Bathroom (O2)",
)


# Now we build lights for OpenOffice East


openofficeEast_luminaire_1 = Luminaire(
    label="Luminaire1",
    comment="Luminaire #1 in OpenOffice East",
    hasPhysicalLocation=ps.openoffice,
    brightnessRatio=0,
    onOffStatus=OnOffStatus(),
    onOffCommand=OnOffCommand(),
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=ElectricPower(13, unit=UNIT.W),
)
openofficeEast_luminaire_2 = Luminaire(
    label="Luminaire2",
    comment="Luminaire #2 in OpenOffice East",
    hasPhysicalLocation=ps.openoffice,
    onOffStatus=OnOffStatus(),
    onOffCommand=OnOffCommand(),
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=ElectricPower(13, unit=UNIT.W),
)
openofficeWest_luminaire_3 = Luminaire(
    label="Luminaire3",
    comment="Luminaire #3 in OpenOffice West",
    hasPhysicalLocation=ps.openoffice,
    onOffStatus=OnOffStatus(),
    onOffCommand=OnOffCommand(),
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=ElectricPower(13, unit=UNIT.W),
)
openofficeWest_luminaire_4 = Luminaire(
    label="Luminaire4",
    comment="Luminaire #4 in OpenOffice West",
    hasPhysicalLocation=ps.openoffice,
    onOffStatus=OnOffStatus(),
    onOffCommand=OnOffCommand(),
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=ElectricPower(13, unit=UNIT.W),
)
# openofficeEast_luminaire_1.lightOutlet >> openofficeEast_lightspace.lightInlet
openofficeEast_light_conn = LightVisibleConnection(
    label="LightHub_1_2", comment="Needed to connect multiple luminaires to space"
)
openofficeWest_light_conn = LightVisibleConnection(
    label="LightHub_3_4", comment="Needed to connect multiple luminaires to space"
)

# Occupancy in OpenOffice comes from 1 sensors for both spaces
openoffice_movement = OccupancySensor(
    label="OccSensor1",
    comment="Occupancy sensor for OpenOffice (O1)",
)

daylight_sensor = DaylightSensor(
    label="Daylight Sensor", comment="Daylight sensor installed in open office (D1)"
)

# Windows are good for natural light
natural_ligth_conn = LightVisibleConnection(
    label="LightHub_NaturalLight",
    comment="2 windows contribute and light is brought to 2 light spaces",
)

if __name__ == "__main__":
    dump()
