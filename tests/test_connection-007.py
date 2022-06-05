from pathlib import Path

from header import ttl_test_header

from bob.connections.air import AirConnection
from bob.connections.electricity import ElectricalInletConnectionPoint
from bob.core import Air, Junction, bind_model_namespace, dump, enum
from bob.devices.hvac.fan import Fan
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.physical import Building, Floor, MechanicalRoom, Office

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_junction_or_connection(bob_fixture):
    building = Building(label="My Building")
    floor = Floor(label="Floor1")
    basement = Floor(label="basement")
    office1 = Office(label="Office 1")
    office2 = Office(label="Office 2")
    office3 = Office(label="Office 3")
    mechroom = MechanicalRoom(label="Mechanical Room")

    office1_hvac = HVACSpace(label="Office 1")
    office2_hvac = HVACSpace(label="Office 2")
    office3_hvac = HVACSpace(label="Office 3")

    zone1 = HVACZone(label="Zone1")

    building > floor
    building > basement
    floor > office1
    floor > office2
    floor > office3
    basement > mechroom
    office1_hvac < office1
    office2_hvac < office2
    office3_hvac < office3

    office1_hvac < zone1
    office2_hvac < zone1

    sf = Fan(
        label="Supply Fan",
        hasPhysicalLocation=mechroom,
    )
    rf = Fan(
        label="Return Fan",
        hasPhysicalLocation=mechroom,
    )

    # Here we make it a junction but it would be better to be a Simple Connection... it's for test purposes
    supply_duct = Junction(label="J1", hasMedium=Air)
    supply_duct.link_to(sf.airOutlet)
    supply_duct >> office1_hvac.ductAirInlet
    supply_duct >> office2_hvac.ductAirInlet
    return_plenum = AirConnection(
        label="RETURN-AIR", comment="Air returns from zone here"
    )
    # return_plenum = Junction(label="J1", hasMedium=Air)
    # return_plenum.link_to(_returnAir.airInlet)
    office1_hvac.ductAirOutlet >> return_plenum
    office2_hvac.ductAirOutlet >> return_plenum
    return_plenum >> rf.airInlet

    # and the zone ?
    zone1.airInlet.mapsTo = supply_duct
    zone1.airOutlet.mapsTo = return_plenum
    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
