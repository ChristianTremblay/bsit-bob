from bob.connections.air import AirConnectionPoint, AirConnection
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.physical import Building, Roof, Floor, Office
from bob.core import dump, turtle, get_datagraph
from bob.devices.hvac.coil import ElectricalHeatingCoil
from bob.connections.air import AirOutletConnectionPoint, AirInletConnectionPoint


def test_create_a_building_and_put_a_heater_1():
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
    AirInJoelsOfficeSpace = AirConnection(label="Air inside the office")
    joelsoffice_hvac.airFromSpace = AirOutletConnectionPoint
    joelsoffice_hvac.airFromBaseboard = AirInletConnectionPoint

    AirInJoelsOfficeSpace << joelsoffice_hvac.airOutlet
    AirInJoelsOfficeSpace >> joelsoffice_hvac.airInlet
    AirInJoelsOfficeSpace << baseboard
    AirInJoelsOfficeSpace >> baseboard


def test_create_a_building_and_put_a_heater_2():
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
    joelsoffice_hvac.airFromSpace = AirOutletConnectionPoint
    joelsoffice_hvac.airFromBaseboard = AirInletConnectionPoint

    joelsoffice_hvac << baseboard
    joelsoffice_hvac >> baseboard


def test_turtle_file():
    dump()
    result = turtle()
    print(result)


if __name__ == "__main__":
    bldg = test_create_a_building_and_put_a_heater_2()

    result = turtle()
    with open("test_device-007_RadiantHeater_results.ttl", "w") as file:
        file.write(result)
    print("Check file : test_device-007_RadiantHeater_results.ttl")
    print(result)
    graph = get_datagraph()
