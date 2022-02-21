from pathlib import Path

from typing import Any

from matplotlib.backend_bases import MouseEvent

from bob.core import (
    System,
    Zone,
    Node,
    s223,
    Segment,
    Junction,
    bind_namespace,
    quantitykind,
    enum,
    turtle,
    get_datagraph,
    bind_model_namespace,
    dump,
)

from bob.devices.hvac.damper import ElectricalActuatedDamper
from bob.devices.hvac.coil import ChilledWaterCoil, HotWaterCoil
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.filter import Filter
from bob.devices.hvac.damper import Window
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

from bob.role import (
    Exhaust,
    Supply,
)
from bob.signal import (
    AnalogOut,
    AnalogIn,
)
from rdflib import Namespace, URIRef, BNode, Literal, RDF, RDFS, XSD

# from header import g36_header


def test_pritoni():
    model_name = "pritoni"
    __namespace__ = ex = bind_model_namespace("ex", f"urn:ex/{model_name}/")

    vav1_config = {
        "params": {"label": "VAVBox1", "comment": "VAV Serving HVAC Zone 1"},
        "sensors": {
            ("VAV1_SA-F", AirFlowSensor): {
                "comment": "Air flow used to control damper"
            },
            ("VAV1_DA-T", AirTemperatureSensor): {
                "comment": "Air supplied to zone by VAV 1, AKA discharge air temperature"
            },
            ("VAV1_ZN-T", AirTemperatureSensor): {
                "comment": "Zone Air Temperature Sensor, which is a thermostats..."
            },
        },
        "contains": {
            ("VAV1_damper", ElectricalActuatedDamper): {
                "comment": "VAV Box 1 Air Damper"
            },
            ("VAV1_HeatingCoil", HotWaterCoil): {"comment": "VAV Box 1 Hot Water Coil"},
        },
    }

    vav2_config = {
        "params": {"label": "VAVBox2", "comment": "VAV Serving HVAC Zone 2"},
        "sensors": {
            ("VAV2_SA-F", AirFlowSensor): {
                "comment": "Air flow used to control damper"
            },
            ("VAV2_DA-T", AirTemperatureSensor): {
                "comment": "Air supplied to zone by VAV 2, AKA discharge air temperature"
            },
            ("VAV2_ZN-T", AirTemperatureSensor): {
                "comment": "Zone Air Temperature Sensor, which is a thermostats..."
            },
        },
        "contains": {
            ("VAV2_damper", ElectricalActuatedDamper): {
                "comment": "VAV Box 2 Air Damper"
            },
            ("VAV2_HeatingCoil", HotWaterCoil): {"comment": "VAV Box 2 Hot Water Coil"},
        },
    }

    # NOT USED YET
    # config = {
    #    "params": {"label": "AHU-1", "comment": "Rooftop Unit"},
    #    "sensors": {
    #        ("DA-T", AirTemperatureSensor): {
    #            "comment": "Supply Air Temperature sensor"
    #        },
    #        ("RA-T", AirTemperatureSensor): {
    #            "comment": "Return Air Temperature sensor"
    #        },
    #        ("ZN-T", AirTemperatureSensor): {"comment": "Zone Air Temperature sensor"},
    #    },
    #    "contains": {
    #        ("SF-1", Fan): {"comment": "Supply Fan"},
    #        ("RF-1", Fan): {"comment": "Return Fan"},
    #        ("OAD-1", ElectricalActuatedDamper): {"comment": "Outside Air Damper"},
    #        ("MAD-1", ElectricalActuatedDamper): {"comment": "Mixed Air Damper"},
    #        ("RAD-1", ElectricalActuatedDamper): {"comment": "Return Air Damper"},
    #        ("CWC-1", ChilledWaterCoil): {"comment": "Chilled Water coil"},
    #        ("HWC-1", HotWaterCoil): {"comment": "Chilled Water coil"},
    #        ("FLT-1", Filter): {"comment": "Filters installe before heating coil"}
    #    },
    # }

    # rtu["OAD-1"] >> mixedAir
    # rtu["RF-1"] >> mixedAir
    # mixedAir >> rtu["SF-1"]
    # rtu["SF-1"] >> rtu["CWC-1"]##

    # Mapping of the system
    # rtu.outsideAirInlet.mapsTo = rtu["OAD-1"].airInlet
    # rtu.returnAirInlet.mapsTo = rtu["RF-1"].airInlet
    # rtu.supplyAirOutlet.mapsTo = rtu["CWC-1"].airOutlet#

    # return_plenum = AirConnection(
    #    label="Return Air Plenum", comment="Air returns from zone here"
    # )
    # return_plenum >> rtu["RF-1"].airInlet
    # supply_duct = AirConnection(
    #    label="Supply Air Duct", comment="Air returns from zone here"
    # )
    # rtu["CWC-1"].airOutlet >> supply_duct
    # rtu["DA-T"].hasMeasurementLocation = supply_duct
    # rtu["RA-T"].hasMeasurementLocation = rtu["RF-1"].airOutlet

    # Define the building Physical Spaces
    bldg = Building(label="Pritoni Building")
    roof = Roof(label="Roof of building")
    floor1 = Floor(label="Floor on which everything is")
    openoffice = Office(label="Open Office")
    bathroom = Bathroom(label="Bathroom")
    private_office = Office(label="Private Office")
    kitchenette = Room(label="Kitchenette")
    corridor = Corridor(label="Corridor")

    # HVAC Spaces
    openoffice_hvac = HVACSpace(label="OpenOffice.HVAC")
    bathroom_hvac = HVACSpace(label="Bathroom.HVAC")
    corridorNorth_hvac = HVACSpace(label="CorridorNorth.HVAC")
    corridorSouth_hvac = HVACSpace(label="CorridorSouth.HVAC")
    privateoffice_hvac = HVACSpace(label="PrivateOffice.HVAC")
    kitchenette_hvac = HVACSpace(label="Kitchenette.HVAC")

    # Light Spaces
    openofficeEast_lightspace = LightingSpace(label="OpenOfficeEast.Light")
    openofficeWest_lightspace = LightingSpace(label="OpenOfficeWest.Light")
    bathroom_lightspace = LightingSpace(label="Bathroom.Light")
    corridor_lightspace = LightingSpace(label="Corridor.Light")
    privateoffice_lightspace = LightingSpace(label="PrivateOffice.Light")
    kitchenette_lightspace = LightingSpace(label="Kitchenette.Light")

    # Relations between Physical spaces and Domain spaces
    bldg > roof
    bldg > floor1
    floor1 > openoffice > openoffice_hvac
    openoffice > openofficeEast_lightspace
    openoffice > openofficeWest_lightspace

    floor1 > bathroom > bathroom_hvac
    bathroom > bathroom_lightspace

    floor1 > corridor > corridorNorth_hvac
    corridor > corridorSouth_hvac
    corridor > corridor_lightspace

    floor1 > private_office > privateoffice_hvac
    private_office > privateoffice_lightspace

    floor1 > kitchenette > kitchenette_hvac
    kitchenette > kitchenette_lightspace

    # Comment
    """
    At this point, it is important to note that the plan we receive may not be in phase
    with the vocabulary of s223. We need to understand the idea behind. When they tell you
    this dash boz is a zone... well, maybe it's a space in our world... maybe it's a zone
    if the idea of system is relevent.

    For example, why do they consider the corridor being in 2 zones... we miss a lot of 
    details here that could help understand. For now though, let's just split this in two : North and South.

    Also, it is clear that Light Zones are in fact Ligth Spaces, as each one contains only 1 device/sensor
    It's not a group of spaces.


    """
    # HVAC Zones
    hvac_zone_1 = HVACZone(
        label="HVACZone1",
        comment="HVAC Zone 1 contains open office, bathroom, private office and corridor north",
    )
    hvac_zone_1 > openoffice_hvac
    hvac_zone_1 > bathroom_hvac
    hvac_zone_1 > corridorNorth_hvac
    hvac_zone_1 > privateoffice_hvac

    hvac_zone_2 = HVACZone(
        label="HVACZone2", comment="HVAC Zone 2 contains Kitchenette and Corridor South"
    )
    hvac_zone_2 > kitchenette_hvac
    hvac_zone_2 > corridorSouth_hvac

    # Comment
    """
    Now looking at the plan, we miss a detail regarding air movement. How is the return air
    dealt with ?

    A single return in the open office ? In this case, air will be forced through doors up 
    to the open office... 

    Return grills in each room open on a big plenum covering the entire floor ?

    Most probably, the bathroom doesn't have a return grill... just an exhaust... but again,
    we miss this information.

    Both scenarios are possible and they will endup being modeled differently

    Based on what we have here, it's impossible to know exactly.

    Knowing that, I'll still try to connect the HVAC Spaces to get the more probably air flow

    """
    corridorNorth_doors = AirConnection(
        label="CorridorNorthDoors",
        comment="There are 3 doors in this space, so I'm using a connection to model those relationships",
    )
    # My model of spaces include 1 input for doors, 1 input for Windows, etc... if there are multiple of those, use a connection.
    kitchenette_hvac.doors >> corridorSouth_hvac
    corridorSouth_hvac.airTransfer >> corridorNorth_hvac.airTransfer

    privateoffice_hvac.doors >> corridorNorth_doors
    bathroom_hvac.doors >> corridorNorth_doors
    openoffice_hvac.doors >> corridorNorth_doors

    outdoor = AirConnection(
        label="Outdoor",
        comment="This is where we exhaust air of bathroom, and windows of OpenOffice are connected here to",
    )

    openoffice_windows = AirConnection(
        label="OpenOfficeWindows",
        comment="There are 2 windows connected to the space, so I use a connection",
    )
    window1 = Window(label="Window#1", comment="First Window in OpenOffice")
    window1.outdoor >> outdoor
    window1.indoor >> openoffice_windows
    window1.hasPhysicalLocation = openoffice
    window2 = Window(label="Window#1", comment="Second Window in OpenOffice")
    window2.outdoor >> outdoor
    window2.indoor >> openoffice_windows
    window2.hasPhysicalLocation = openoffice
    openoffice_windows >> openoffice_hvac.windows

    bathroom_exhaust_fan = Fan(label="ExhaustFan", comment="Bathroom exhaust fan")
    bathroom_exhaust_fan.airInlet << bathroom_hvac
    bathroom_exhaust_fan.airOutlet >> outdoor

    # Now we build HVAC devices
    supplyAir = AirConnection(
        label="SUPPLY-DUCT", comment="Supply Air Duct that feed VAV Boxes 1 & 2"
    )

    returnAir = AirConnection(
        label="RETURN-DUCT", comment="Return Air Duct extracting air from open office"
    )

    vav1 = VAV(config=vav1_config)
    vav1.servesZone = hvac_zone_1
    vav2 = VAV(config=vav2_config)
    vav2.servesZone = hvac_zone_2

    # Relationships between devices and positioning sensors
    supplyAir >> vav1["VAV1_damper"].airInlet
    vav1["VAV1_damper"].airOutlet >> vav1["VAV1_HeatingCoil"].airInlet
    vav1["VAV1_HeatingCoil"].airOutlet >> privateoffice_hvac.ductAirInlet
    vav1["VAV1_SA-F"].hasMeasurementLocation = vav1["VAV1_damper"].airInlet
    vav1["VAV1_DA-T"].hasMeasurementLocation = vav1["VAV1_HeatingCoil"].airOutlet
    vav1["VAV1_ZN-T"].hasMeasurementLocation = openoffice_hvac
    vav1["VAV1_ZN-T"].hasPhysicalLocation = openoffice

    supplyAir >> vav2["VAV2_damper"].airInlet
    vav2["VAV2_damper"].airOutlet >> vav2["VAV2_HeatingCoil"].airInlet
    vav2["VAV2_HeatingCoil"].airOutlet >> kitchenette_hvac.ductAirInlet
    vav2["VAV2_SA-F"].hasMeasurementLocation = vav2["VAV2_damper"].airInlet
    vav2["VAV2_DA-T"].hasMeasurementLocation = vav2["VAV2_HeatingCoil"].airOutlet
    vav2["VAV2_ZN-T"].hasMeasurementLocation = corridorSouth_hvac
    vav2["VAV2_ZN-T"].hasPhysicalLocation = corridor

    # Now we build lights for Kitchenette
    kitchenette_bulb = Light(label="Bulb1_Kitch", comment="Light Bulb in kitchenette")
    kitchenette_movement = MovementSensor(
        label="Bulb1_Mov", comment="Movement sensor for kitchenette bulb 1"
    )
    kitchenette_bulb.lightOutlet >> kitchenette_lightspace.lightInlet
    kitchenette_movement.hasMeasurementLocation = kitchenette_lightspace
    kitchenette_movement.hasPhysicalLocation = kitchenette

    # Now we build lights for Private Office
    privateoffice_bulb = Light(
        label="Bulb2_PrivateOffice", comment="Light Bulb in Private Office"
    )
    privateoffice_movement = MovementSensor(
        label="Bulb2_Mov", comment="Movement sensor for Privtae Office bulb"
    )
    privateoffice_bulb.lightOutlet >> privateoffice_lightspace.lightInlet
    privateoffice_movement.hasMeasurementLocation = privateoffice_lightspace
    privateoffice_movement.hasPhysicalLocation = private_office

    # Now we build lights for Corridor
    corridor_bulb = Light(label="Bulb3_Corridor", comment="Light Bulb in Corridor")
    corridor_movement = MovementSensor(
        label="Bulb3_Mov", comment="Movement sensor for Corridor bulb"
    )
    corridor_bulb.lightOutlet >> corridor_lightspace.lightInlet
    corridor_movement.hasMeasurementLocation = corridor_lightspace
    corridor_movement.hasPhysicalLocation = corridor

    # Now we build lights for Bathroom
    bathroom_bulb = Light(label="Bulb4_Corridor", comment="Light Bulb in Bathroom")
    bathroom_movement = MovementSensor(
        label="Bulb4_Mov", comment="Movement sensor for Bathroom bulb"
    )
    bathroom_bulb.lightOutlet >> bathroom_lightspace.lightInlet
    bathroom_movement.hasMeasurementLocation = bathroom_lightspace
    bathroom_movement.hasPhysicalLocation = bathroom

    # Now we build lights for OpenOffice East
    openofficeEast_bulb = Light(
        label="Bulb5_OpenOfficeE", comment="Light Bulb in OpenOffice E"
    )
    openofficeEast_movement = MovementSensor(
        label="Bulb5_Mov", comment="Movement sensor for OpenOffice East"
    )
    openofficeEast_bulb.lightOutlet >> openofficeEast_lightspace.lightInlet
    openofficeEast_movement.hasMeasurementLocation = openofficeEast_lightspace
    openofficeEast_movement.hasPhysicalLocation = openoffice

    # Now we build lights for OpenOffice West
    openofficeWest_bulb = Light(
        label="Bulb5_OpenOfficeW", comment="Light Bulb in OpenOffice A"
    )
    openofficeWest_movement = MovementSensor(
        label="Bulb6_Mov", comment="Movement sensor for Open Office West"
    )
    openofficeWest_bulb.lightOutlet >> openofficeWest_lightspace.lightInlet
    openofficeWest_movement.hasMeasurementLocation = openofficeWest_lightspace
    openofficeWest_movement.hasPhysicalLocation = openoffice

    # More connections on systems and zones (mapping)

    hvac_zone_1.airInlet.mapsTo = privateoffice_hvac.ductAirInlet
    hvac_zone_1.airOutlet.mapsTo = openoffice_hvac.ductAirOutlet

    hvac_zone_2.airInlet.mapsTo = kitchenette_hvac.ductAirInlet
    hvac_zone_2.airOutlet.mapsTo = corridorSouth_hvac.airTransfer

    # Would be nice to make this when we create the system...
    vav1.airInlet.mapsTo = vav1["VAV1_damper"].airInlet
    vav1.airOutlet.mapsTo = vav1["VAV1_HeatingCoil"].airOutlet
    vav2.airInlet.mapsTo = vav2["VAV2_damper"].airInlet
    vav2.airOutlet.mapsTo = vav2["VAV2_HeatingCoil"].airOutlet


if __name__ == "__main__":
    r = test_pritoni()
    result = turtle()
    with open("tests/ttl/Pritoni.ttl", "w") as file:
        file.write(result)
    print("Check file : tests/ttl/Pritoni.ttl")
    print(result)
    graph = get_datagraph()
