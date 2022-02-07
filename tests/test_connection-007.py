from bob.core import (
    bind_model_namespace,
    dump,
    turtle,
    ExternalReference,
    get_datagraph,
    Value,
    quantitykind,
    unit,
    enum,
    Device,
    Junction,
)
from rdflib import URIRef

from bob.devices.electricity.distribution_wip import DistributionPanel, CircuitBreaker
from bob.connections.electricity import (
    Electricity_120V_60HzInletConnectionPoint,
    Electricity_120V_60HzOutletConnectionPoint,
    Electricity_240V_60HzInletConnectionPoint,
    Electricity_240V_60HzOutletConnectionPoint,
    Electricity_120V_240V_60HzInletConnectionPoint,
)
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.physical import Building, Floor, MechanicalRoom, Office
from bob.core import DomainSpace, HVAC, PhysicalSpace
from bob.devices.hvac.fan import Fan
from bob.connections.air import AirConnection

__namespace__ = bind_model_namespace("ex", "urn:ex/")


def test_make_connections_in_building():
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

    sf = Fan(label="Supply Fan", hasLocation=mechroom)
    rf = Fan(label="Return Fan", hasLocation=mechroom)
    # Here we make it a junction but it would be better to be a Simple Connection... it's for test purposes
    supply_duct = Junction(label="J1", hasSubstance=enum["Medium-Air"])
    supply_duct.link_to(sf.airOutlet)
    supply_duct >> office1_hvac.airInlet
    supply_duct >> office2_hvac.airInlet
    return_plenum = AirConnection(
        label="RETURN-AIR", comment="Air returns from zone here"
    )
    # return_plenum = Junction(label="J1", hasSubstance=enum['Medium-Air'])
    # return_plenum.link_to(_returnAir.airInlet)
    office1_hvac.airOutlet >> return_plenum
    office2_hvac.airOutlet >> return_plenum
    return_plenum >> rf

    # and the zone ?
    zone1.airInlet.mapsTo = supply_duct
    zone1.airOutlet.mapsTo = return_plenum


def test_turtle_file():
    dump()
    result = turtle()
    print(result)


if __name__ == "__main__":
    panel = test_make_connections_in_building()
    # panel2 = test_create_emptyelectricalpaneldevice()
    result = turtle()
    with open("test_connection-007_results.ttl", "w") as file:
        file.write(result)
    print("Check file : test_connection-007_results.ttl")
    print(result)
    graph = get_datagraph()
