from cProfile import label
from pathlib import Path

from typing import Any

from bob.connections.light import LightVisibleConnection
from bob.connections.occupancy import (
    OccupancyInletSystemConnectionPoint,
    OccupancyOutletSystemConnectionPoint,
)

from bob.core import p223, get_datagraph, bind_model_namespace, dump, quantitykind, unit

from bob.devices.hvac.damper import ElectricalActuatedDamper
from bob.devices.hvac.coil import ChilledWaterCoil, HotWaterCoil
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.filter import Filter
from bob.devices.hvac.damper import Window
from bob.devices.lighting.light import Luminaire

from bob.devices.electricity.distribution import (
    DistributionPanel,
    Transformer,
    SinglePhaseDistributionPanel,
    SinglePoleCircuitBreaker,
    ThreePhasesDistributionPanel,
    ThreePolesCircuitBreaker,
    ThreePolesMainCircuitBreaker,
    TwoPolesCircuitBreaker,
    TwoPolesMainCircuitBreaker,
)
from bob.property import QuantifiableObservableProperty

from bob.space.occupancy import OccupancySpace
from bob.systems.hvac.airhandlingunit import AirHandlingUnit
from bob.systems.hvac.vav import VAV
from bob.sensor.temperature import AirTemperatureSensor
from bob.sensor.flow import AirFlowSensor
from bob.sensor.movement import MovementSensor, OccupancySensor

from bob.space.physical import Building, Floor, Roof, Office, Room, Bathroom, Corridor
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.light import LightingSpace, LightingZone

from bob.systems.functionblock import FunctionBlock

from bob.connections.air import *
from bob.connections.electricity import *

from header import sample_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")

mainentry_panel_config = {
    "params": {
        "label": "Main Entry Panel",
        "comment": "Main Entry Panel of Building at 575V",
        "voltage": "575",
    },
    "sensors": {},
    "contains": {
        ("MainBreaker", ThreePolesMainCircuitBreaker): {
            "comment": "Main breaker of panel",
            "amps": 400,
            "voltage": "575",
        },
        ("CB#1", SinglePoleCircuitBreaker): {
            "comment": "Parking Lot Lights",
            "amps": 15,
            "voltage": 347,
            "bus_bar": "A",
        },
        ("CB#2", ThreePolesCircuitBreaker): {
            "comment": "Fans, AHU",
            "amps": 40,
            "voltage": "575",
        },
        ("CB#3", ThreePolesCircuitBreaker): {
            "comment": "Feeds Transformer to get 120/240",
            "amps": 100,
            "voltage": "575",
        },
    },
    # other properties could go there... ?
}

distribution_panel_config = {
    "params": {
        "label": "My Panel",
        "comment": "Description of my panel",
        "voltage": "120_240",
    },
    "sensors": {},
    "contains": {
        ("MainBreaker", TwoPolesMainCircuitBreaker): {
            "comment": "Main breaker of panel",
            "amps": 200,
            "voltage": "120_240",
        },
        ("CB#1", SinglePoleCircuitBreaker): {
            "comment": "Lights in OpenOffice",
            "amps": 15,
            "voltage": "120",
            "bus_bar": "A",
        },
        ("CB#2", TwoPolesCircuitBreaker): {
            "comment": "Heater",
            "amps": 20,
            "voltage": "240",
        },
        ("CB#3", SinglePoleCircuitBreaker): {
            "comment": "Lights in Kitchenette",
            "amps": 15,
            "voltage": "120",
            "bus_bar": "A",
        },
        ("CB#4", SinglePoleCircuitBreaker): {
            "comment": "Lights in Corridors + bathroom",
            "amps": 15,
            "voltage": "120",
            "bus_bar": "A",
        },
        ("CB#5", SinglePoleCircuitBreaker): {
            "comment": "Lights in Private Office",
            "amps": 15,
            "voltage": "120",
            "bus_bar": "A",
        },
    },
    # other properties could go there... ?
}


def test_pritoni():
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
    openoffice_hvac = HVACSpace(label="HVACSpace1", comment="OpenOffice.HVAC")
    bathroom_hvac = HVACSpace(label="HVACSpace2", comment="Bathroom.HVAC")
    corridorNorth_hvac = HVACSpace(label="HVACSpace4", comment="CorridorNorth.HVAC")
    corridorSouth_hvac = HVACSpace(label="HVACSpace5", comment="CorridorSouth.HVAC")
    privateoffice_hvac = HVACSpace(label="HVACSpace3", comment="PrivateOffice.HVAC")
    kitchenette_hvac = HVACSpace(label="HVACSpace6", comment="Kitchenette.HVAC")

    # Light Spaces
    openofficeEast_lightspace = LightingSpace(
        label="LightingSpace1", comment="OpenOfficeEast.Light"
    )
    openofficeWest_lightspace = LightingSpace(
        label="LightingSpace2", comment="OpenOfficeWest.Light"
    )
    bathroom_lightspace = LightingSpace(
        label="LightingSpace3", comment="Bathroom.Light"
    )
    corridor_lightspace = LightingSpace(
        label="LightingSpace5", comment="Corridor.Light"
    )
    privateoffice_lightspace = LightingSpace(
        label="LightingSpace4", comment="PrivateOffice.Light"
    )
    kitchenette_lightspace = LightingSpace(
        label="LightingSpace6", comment="Kitchenette.Light"
    )

    # Occupancy Spaces
    openoffice_occ_space = OccupancySpace(
        label="OccupancySpace1", comment="Occupancy space of Open Office"
    )
    kitchenette_occ_space = OccupancySpace(
        label="OccupancySpace6", comment="Occupancy Space of kitechnette"
    )

    # Electrical devices
    main_panel = ThreePhasesDistributionPanel(config=mainentry_panel_config)
    transformer_120_240 = Transformer(
        label="TX-1",
        electricalInlet=Electricity_575V_60HzInletConnectionPoint,
        electricalOutlet=Electricity_120V_240V_60HzOutletConnectionPoint,
    )

    dist_panel = SinglePhaseDistributionPanel(config=distribution_panel_config)
    # hq = Electricity_120V_240V_60HzConnection(label='Hydro-Québec', comment="That would be for a home...")
    hq_600 = Electricity_575V_60HzConnection(label="Hydro-Québec", comment="600V")
    hq_600 >> main_panel["MainBreaker"]
    main_panel["CB#3"] >> transformer_120_240 >> dist_panel["MainBreaker"]
    # main_panel['CB#2'] >> Fans...

    # We need a truff so light breakers will be connected to multiple loads
    dist_panel_cb1 = Electricity_120V_60HzConnection(label="DISTPANEL-CB1")
    dist_panel_cb3 = Electricity_120V_60HzConnection(label="DISTPANEL-CB3")
    dist_panel_cb4 = Electricity_120V_60HzConnection(label="DISTPANEL-CB4")
    dist_panel_cb5 = Electricity_120V_60HzConnection(label="DISTPANEL-CB5")
    dist_panel["CB#1"] >> dist_panel_cb1
    dist_panel["CB#3"] >> dist_panel_cb3
    dist_panel["CB#4"] >> dist_panel_cb4
    dist_panel["CB#5"] >> dist_panel_cb5

    # hq >> main_panel['MainBreaker']
    # main_panel['CB#1'] >> transformer_120_240 >> dist_panel['MainBreaker']
    # main_panel['CB#2'] >> AHU ???

    # Relations between Physical spaces and Domain spaces
    bldg > roof
    bldg > floor1
    floor1 > openoffice > openoffice_hvac
    openoffice > openofficeEast_lightspace
    openoffice > openofficeWest_lightspace
    openoffice > openoffice_occ_space

    floor1 > bathroom > bathroom_hvac
    bathroom > bathroom_lightspace

    floor1 > corridor > corridorNorth_hvac
    corridor > corridorSouth_hvac
    corridor > corridor_lightspace

    floor1 > private_office > privateoffice_hvac
    private_office > privateoffice_lightspace

    floor1 > kitchenette > kitchenette_hvac
    kitchenette > kitchenette_lightspace
    kitchenette > kitchenette_occ_space

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

    # Lighting Zones
    lighting_zone_1 = LightingZone(
        label="LightingZone1", comment="Contains OpenOffice Space West"
    )
    lighting_zone_1 > openofficeWest_lightspace
    lighting_zone_2 = LightingZone(
        label="LightingZone2", comment="Contains OpenOffice Space East"
    )
    lighting_zone_2 > openofficeEast_lightspace

    lighting_zone_3 = LightingZone(
        label="LightingZone3", comment="Contains Bathroom Light Space"
    )
    lighting_zone_3 > bathroom_lightspace

    lighting_zone_4 = LightingZone(
        label="LightingZone4", comment="Contains Private Office Light Space"
    )
    lighting_zone_4 > privateoffice_lightspace

    lighting_zone_5 = LightingZone(
        label="LightingZone5", comment="Contains Corridor Light Space"
    )
    lighting_zone_5 > corridor_lightspace

    lighting_zone_6 = LightingZone(
        label="LightingZone6", comment="Contains Kitchenette Light Space"
    )
    lighting_zone_6 > kitchenette_lightspace

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
    kitchenette_hvac.doors >> corridorSouth_hvac.doors
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
    window1 = Window(
        label="Window_West",
        comment="First Window in OpenOffice, covering West portion of room",
    )
    window1.outdoor >> outdoor
    window1.indoor >> openoffice_windows
    window1.hasPhysicalLocation = openoffice
    window2 = Window(
        label="Window_East",
        comment="Second Window in OpenOffice, covering East portion of room",
    )
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
    kitchenette_luminaire_11 = Luminaire(
        label="Luminaire11",
        comment="Luminaire in kitchenette #11",
    )
    kitchenette_luminaire_12 = Luminaire(
        label="Luminaire12",
        comment="Luminaire in kitchenette #12",
    )
    kitchenette_movement = OccupancySensor(
        label="OccSensor5",
        comment="Occupancy sensor for kitchenette luminaires 11 & 12",
    )
    kitch_light_conn = LightVisibleConnection(
        label="LightHub_11_12", comment="Needed to connect multiple luminaires to space"
    )
    kitchenette_luminaire_11.lightOutlet >> kitch_light_conn
    kitchenette_luminaire_12.lightOutlet >> kitch_light_conn
    kitch_light_conn >> kitchenette_lightspace.lightInlet

    # There is a occupancy space for Kitchenette... go figure
    kitchenette_movement.hasMeasurementLocation = kitchenette_occ_space
    kitchenette_movement.hasPhysicalLocation = kitchenette

    # Now we build lights for Private Office
    privateoffice_luminaire_7 = Luminaire(
        label="Luminaire7",
        comment="Luminaire #7 in Private Office",
        hasPhysicalLocation=private_office,
    )
    privateoffice_luminaire_8 = Luminaire(
        label="Luminaire8",
        comment="Luminaire #8 in Private Office",
        hasPhysicalLocation=private_office,
    )
    privateoffice_movement = MovementSensor(
        label="OccSensor3",
        comment="Occupancy sensor for Privtae Office",
        hasPhysicalLocation=private_office,
        hasMeasurementLocation=privateoffice_lightspace,
    )
    privateoffice_light_conn = LightVisibleConnection(
        label="LightHub_7_8", comment="Needed to connect multiple luminaires to space"
    )

    privateoffice_luminaire_7.lightOutlet >> privateoffice_light_conn
    privateoffice_luminaire_8.lightOutlet >> privateoffice_light_conn
    privateoffice_light_conn >> privateoffice_lightspace.lightInlet

    # privateoffice_movement.hasMeasurementLocation = privateoffice_lightspace
    # privateoffice_movement.hasPhysicalLocation = private_office

    # Now we build lights for Corridor
    corridor_luminaire_9 = Luminaire(
        label="Luminaire9",
        comment="Luminaire #9 in Corridor",
        hasPhysicalLocation=corridor,
    )
    corridor_luminaire_10 = Luminaire(
        label="Luminaire10",
        comment="Luminaire #10 in Corridor",
        hasPhysicalLocation=corridor,
    )
    corridor_movement = OccupancySensor(
        label="OccSensor4", comment="Occupancy sensor for Corridor"
    )
    corridor_light_conn = LightVisibleConnection(
        label="LightHub_9_10", comment="Needed to connect multiple luminaires to space"
    )
    corridor_luminaire_9.lightOutlet >> corridor_light_conn
    corridor_luminaire_10.lightOutlet >> corridor_light_conn
    corridor_light_conn >> corridor_lightspace.lightInlet

    corridor_movement.hasMeasurementLocation = corridor_lightspace
    corridor_movement.hasPhysicalLocation = corridor

    # Now we build lights for Bathroom
    bathroom_luminaire_5 = Luminaire(
        label="Luminaire5",
        comment="Luminaire #5 in Bathroom",
        hasPhysicalLocation=bathroom,
    )
    bathroom_luminaire_6 = Luminaire(
        label="Luminaire6",
        comment="Luminaire #6 in Bathroom",
        hasPhysicalLocation=bathroom,
    )
    bathroom_light_conn = LightVisibleConnection(
        label="LightHub_5_6", comment="Needed to connect multiple luminaires to space"
    )
    bathroom_movement = OccupancySensor(
        label="OccSensor2", comment="Occupancy sensor for Bathroom"
    )
    bathroom_luminaire_5.lightOutlet >> bathroom_light_conn
    bathroom_luminaire_6.lightOutlet >> bathroom_light_conn
    bathroom_light_conn >> bathroom_lightspace.lightInlet
    bathroom_movement.hasMeasurementLocation = bathroom_lightspace
    bathroom_movement.hasPhysicalLocation = bathroom

    # Now we build lights for OpenOffice East
    openofficeEast_luminaire_1 = Luminaire(
        label="Luminaire1",
        comment="Luminaire #1 in OpenOffice East",
        hasPhysicalLocation=openoffice,
    )
    openofficeEast_luminaire_2 = Luminaire(
        label="Luminaire2",
        comment="Luminaire #2 in OpenOffice East",
        hasPhysicalLocation=openoffice,
    )
    openofficeWest_luminaire_3 = Luminaire(
        label="Luminaire3",
        comment="Luminaire #3 in OpenOffice West",
        hasPhysicalLocation=openoffice,
    )
    openofficeWest_luminaire_4 = Luminaire(
        label="Luminaire4",
        comment="Luminaire #4 in OpenOffice West",
        hasPhysicalLocation=openoffice,
    )
    # openofficeEast_luminaire_1.lightOutlet >> openofficeEast_lightspace.lightInlet

    openofficeEast_light_conn = LightVisibleConnection(
        label="LightHub_1_2", comment="Needed to connect multiple luminaires to space"
    )
    openofficeWest_light_conn = LightVisibleConnection(
        label="LightHub_3_4", comment="Needed to connect multiple luminaires to space"
    )
    openofficeEast_luminaire_1.lightOutlet >> openofficeEast_light_conn
    openofficeEast_luminaire_2.lightOutlet >> openofficeEast_light_conn
    openofficeEast_light_conn >> openofficeEast_lightspace.lightInlet

    openofficeWest_luminaire_3.lightOutlet >> openofficeWest_light_conn
    openofficeWest_luminaire_4.lightOutlet >> openofficeWest_light_conn
    openofficeWest_light_conn >> openofficeWest_lightspace.lightInlet

    # Occupancy in OpenOffice comes from 1 sensors for both spaces
    openofficeEast_movement = OccupancySensor(
        label="OccSensor1", comment="Occupancy sensor for OpenOffice"
    )

    openofficeEast_movement.hasMeasurementLocation = openoffice_occ_space
    openofficeEast_movement.hasPhysicalLocation = openoffice

    # Windows are good for natural light
    natural_ligth_conn = LightVisibleConnection(
        label="LightHub_NaturalLight",
        comment="2 windows contribute and light is brought to 2 light spaces",
    )
    window1.naturalLight >> natural_ligth_conn
    window2.naturalLight >> natural_ligth_conn
    natural_ligth_conn >> openofficeEast_lightspace.naturalLightInlet
    natural_ligth_conn >> openofficeWest_lightspace.naturalLightInlet

    # Windows are good for natural light
    # window1.naturalLight >> openofficeWest_lightspace.naturalLightInlet
    # window2.naturalLight >> openofficeEast_lightspace.naturalLightInlet

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

    # Occupancies are shared between space... let's build a function block to relate them
    class OccupancyControl(FunctionBlock):
        node_type = p223.OccupancyControl
        occupancySensor: OccupancyInletSystemConnectionPoint
        occupancyZone1: OccupancyOutletSystemConnectionPoint
        occupancyZone2: OccupancyOutletSystemConnectionPoint

    open_office_occ_control = OccupancyControl(
        label="OpenOffice Occ Control",
        comment="Occupancy sensor drives LightingZone1 and LightingZone2",
    )
    open_office_occ_control.occupancySensor.mapsTo = openofficeEast_movement
    open_office_occ_control.occupancyZone1.mapsTo = lighting_zone_1
    open_office_occ_control.occupancyZone2.mapsTo = lighting_zone_2

    kitchenette_occ_control = OccupancyControl(
        label="Kitchenette Occ Control",
        comment="Deal with OccupancySpace6...probably not required but it's defined",
    )
    kitchenette_occ_control.occupancySensor.mapsTo = kitchenette_movement
    kitchenette_occ_control.occupancyZone1.mapsTo = lighting_zone_6

    # Make Electrical connections
    dist_panel_cb1 >> [
        openofficeEast_luminaire_1,
        openofficeEast_luminaire_2,
        openofficeWest_luminaire_3,
        openofficeWest_luminaire_4,
    ]
    dist_panel_cb3 >> [
        kitchenette_luminaire_11,
        kitchenette_luminaire_12,
    ]

    dist_panel_cb4 >> [
        bathroom_luminaire_5,
        bathroom_luminaire_6,
        corridor_luminaire_9,
        corridor_luminaire_10,
    ]

    dist_panel_cb5 >> [
        privateoffice_luminaire_7,
        privateoffice_luminaire_8,
    ]


if __name__ == "__main__":
    r = test_pritoni()
    dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
