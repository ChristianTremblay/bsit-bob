import logging

logging.basicConfig(level=logging.DEBUG)

from pathlib import Path
from typing import Any

from header import sample_header
from rdflib import RDF, RDFS, XSD, BNode, Literal, Namespace, URIRef

from bob.connections.air import *
from bob.connections.electricity import ElectricalInletConnectionPoint
from bob.core import (
    Junction,
    Node,
    Segment,
    System,
    Zone,
    bind_model_namespace,
    bind_namespace,
    dump,
    enum,
    get_datagraph,
    QUANTITYKIND,
    S223,
    UNIT,
)
from bob.devices.hvac.coil import ChilledWaterCoil
from bob.devices.hvac.damper import ElectricalActuatedProportionalDamper
from bob.devices.hvac.fan import Fan
from bob.enum import Exhaust, Supply
from bob.sensor.temperature import AirTemperatureSensor
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.physical import Building, Floor, Office, Roof
from bob.systems.hvac.airhandlingunit import AirHandlingUnit

# from header import g36_header

# model_name = Path(__file__).stem
model_name = "B59"
_namespace = ex = bind_model_namespace("ex", f"urn:ex/{model_name}/")


config = {
    "params": {
        # "node_iri": node_iri,
        "label": "RTU-1",
        "comment": "Rooftop Unit",
    },
    "sensors": {
        ("DA-T", AirTemperatureSensor): {
            "comment": "Supply Air Temperature sensor",
            "unit": UNIT.DEG_C,
        },
        ("RA-T", AirTemperatureSensor): {
            "comment": "Return Air Temperature sensor",
            "unit": UNIT.DEG_C,
        },
        ("ZN-T", AirTemperatureSensor): {
            "comment": "Zone Air Temperature sensor",
            "unit": UNIT.DEG_C,
        },
    },
    "devices": {
        ("SF-1", Fan): {
            "comment": "Supply Fan",
            "electricalInlet": ElectricalInletConnectionPoint,
        },
        ("RF-1", Fan): {
            "comment": "Return Fan",
            "electricalInlet": ElectricalInletConnectionPoint,
        },
        ("OAD-1", ElectricalActuatedProportionalDamper): {
            "comment": "Outside Air Damper"
        },
        ("RAD-1", ElectricalActuatedProportionalDamper): {
            "comment": "Return Air Damper"
        },
        ("CWC-1", ChilledWaterCoil): {"comment": "Chilled Water coil"},
    },
}

# rtu is a System
rtu = AirHandlingUnit(config=config)

mixedAir = AirConnection(
    label="MIXED-AIR", comment="Where return air and outside air mix"
)

# Relationships between devices
rtu["OAD-1"] >> mixedAir
rtu["RF-1"] >> mixedAir
mixedAir >> rtu["SF-1"].airInlet
rtu["SF-1"].airOutlet >> rtu["CWC-1"].airInlet

# Mapping of the system
rtu.outsideAirInlet.mapsTo = rtu["OAD-1"].airInlet
rtu.returnAirInlet.mapsTo = rtu["RF-1"].airInlet
rtu.supplyAirOutlet.mapsTo = rtu["CWC-1"].airOutlet

return_plenum = AirConnection(
    label="Return Air Plenum", comment="Air returns from zone here"
)
return_plenum >> rtu["RF-1"].airInlet
supply_duct = AirConnection(
    label="Supply Air Duct", comment="Air returns from zone here"
)
rtu["CWC-1"].airOutlet >> supply_duct
rtu["DA-T"].hasMeasurementLocation = supply_duct
rtu["RA-T"].hasMeasurementLocation = rtu["RF-1"].airOutlet

bldg = Building(label="B59 Building")
roof = Roof(label="Roof of building")
floor1 = Floor(label="One big floor which is a common space")
office1 = Office(label="Director Office")
floor1_hvacspace = HVACSpace(label="HVAC Space for floor 1")
rtu_zone = HVACZone(label="Common workspace zone for HVAC")

bldg > floor1 > floor1_hvacspace
bldg > roof
floor1 > office1

supply_duct >> floor1_hvacspace.ductAirInlet
floor1_hvacspace.ductAirOutlet >> return_plenum

rtu_zone > floor1_hvacspace
rtu_zone.airInlet.mapsTo = supply_duct
rtu_zone.airOutlet.mapsTo = return_plenum

rtu.hasPhysicalLocation = roof
rtu["ZN-T"].hasMeasurementLocation = floor1_hvacspace.ductAirOutlet
rtu["ZN-T"].hasPhysicalLocation = office1
rtu["DA-T"].hasPhysicalLocation = floor1
rtu["RA-T"].hasPhysicalLocation = roof

# Should a plenum be a segment or is system correct??
# class Plenum(AirConnection):
#    AirInlet: AirInletSystemConnectionPoint  # would the outlet be a junction, or just connection points??
#    AirOutlet: AirOutletSystemConnectionPoint
#    hasMedium = Air##

#    def __init__(self, **kwargs: Any) -> None:
#        super().__init__(**kwargs)
#        j = Junction(label=self.label + ".inlet")
#        # j.hasMedium = Air
#        j2 = Junction(label=self.label + ".outlet")
#        # j2.hasMedium = Air #If the junction has a substance, then it doesn't connect. Am I just doing this wrong??
#        self.AirInlet.mapsTo = j
#        self.AirOutlet.mapsTo = j2


# make an instance
# class HVACZone2(HVACZone):
#    node_type = None  # Does this just mean that this isn't something in 223p yet?
#    temperature_setpoint: AnalogOut###

#    def __init__(self, label: str) -> None:
#        super().__init__(label=label)
#        # I need a junction to be the system inlet and outlet if I want to connect to another junction.
#        j = Junction()
#        self.supplyAir.mapsTo = j#


# r = RooftopUnit(node_iri=ex.rtu, label="rtu")
# p = Plenum(label="plenum")
# z = HVACZone2(label="zone")
# can't seem to connect system connection points to junctions
# r.supplyAirOutlet >> p.AirInlet

# p.AirOutlet.link_to(z.supplyAir) #getting no common connection types, because supply Air isn't a junction
# p.AirOutlet >> (z.supplyAir)

# g36_header(model_name)

dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
