from bob.devices.lighting.light import *
from bob.connections.light import *
from bob.externalreference.bacnet import BACnetReference
from bob.sensor.movement import OccupancySensor
from bob.properties.light import RelativeLuminousFlux
import lighting_spaces as ls
import physical_spaces as ps


# Now we build lights for Kitchenette
kitchenette_luminaire_11 = Luminaire(
    label="Luminaire11",
    comment="Luminaire in kitchenette #11",
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=100,
)
kitchenette_luminaire_12 = Luminaire(
    label="Luminaire12",
    comment="Luminaire in kitchenette #12",
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=100,
)
kitchenette_movement = OccupancySensor(
    label="OccSensor5",
    comment="Occupancy sensor for kitchenette luminaires 11 & 12",
)
kitch_light_conn = LightVisibleConnection(
    label="LightHub_11_12", comment="Needed to connect multiple luminaires to space"
)


# Now we build lights for Private Office
privateoffice_luminaire_7 = Luminaire(
    label="Luminaire7",
    comment="Luminaire #7 in Private Office",
    hasPhysicalLocation=ps.private_office,
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=60,
)
privateoffice_luminaire_8 = Luminaire(
    label="Luminaire8",
    comment="Luminaire #8 in Private Office",
    hasPhysicalLocation=ps.private_office,
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=60,
)
privateoffice_movement = MovementSensor(
    label="OccSensor3",
    comment="Occupancy sensor for Privtae Office",
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
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=100,
    hasOnOffStatus=OnOffStatus(hasValue=1),
)
corridor_luminaire_10 = Luminaire(
    label="Luminaire10",
    comment="Luminaire #10 in Corridor",
    hasPhysicalLocation=ps.corridor,
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=100,
    hasOnOffStatus=OnOffStatus(hasValue=1),
)
corridor_movement = OccupancySensor(
    label="OccSensor4", comment="Occupancy sensor for Corridor"
)
corridor_light_conn = LightVisibleConnection(
    label="LightHub_9_10", comment="Needed to connect multiple luminaires to space"
)


# Now we build lights for Bathroom
bathroom_luminaire_5 = Luminaire(
    label="Luminaire5",
    comment="Luminaire #5 in Bathroom",
    hasPhysicalLocation=ps.bathroom,
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=60,
    hasOnOffStatus=OnOffStatus(hasValue=0),
)
bathroom_luminaire_6 = Luminaire(
    label="Luminaire6",
    comment="Luminaire #6 in Bathroom",
    hasPhysicalLocation=ps.bathroom,
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=60,
)
bathroom_light_conn = LightVisibleConnection(
    label="LightHub_5_6", comment="Needed to connect multiple luminaires to space"
)
bathroom_movement = OccupancySensor(
    label="OccSensor2", comment="Occupancy sensor for Bathroom"
)


# Now we build lights for OpenOffice East
openofficeEast_luminaire_1 = Luminaire(
    label="Luminaire1",
    comment="Luminaire #1 in OpenOffice East",
    hasPhysicalLocation=ps.openoffice,
    brightnessRatio=0,
    hasOnOffStatus=OnOffStatus(),
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=13,
)
openofficeEast_luminaire_2 = Luminaire(
    label="Luminaire2",
    comment="Luminaire #2 in OpenOffice East",
    hasPhysicalLocation=ps.openoffice,
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=13,
)
openofficeWest_luminaire_3 = Luminaire(
    label="Luminaire3",
    comment="Luminaire #3 in OpenOffice West",
    hasPhysicalLocation=ps.openoffice,
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=13,
)
openofficeWest_luminaire_4 = Luminaire(
    label="Luminaire4",
    comment="Luminaire #4 in OpenOffice West",
    hasPhysicalLocation=ps.openoffice,
    electricalInlet=Electricity_120V_60HzInletConnectionPoint,
    electricalPower=13,
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
    label="OccSensor1", comment="Occupancy sensor for OpenOffice"
)


# Windows are good for natural light
natural_ligth_conn = LightVisibleConnection(
    label="LightHub_NaturalLight",
    comment="2 windows contribute and light is brought to 2 light spaces",
)
