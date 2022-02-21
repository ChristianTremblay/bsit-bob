from bob.space.hvac import HVACSpace, HVACZone
from bob.space.physical import Building, Roof, Floor, Office
from bob.core import dump, turtle, get_datagraph, bind_model_namespace

from pathlib import Path

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_a_building():
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

    zone1 = HVACZone(label="Zone1")

    # Physical relationships
    building > roof
    building > floor
    building > basement
    floor > office1
    floor > office2
    floor > office3
    basement > joelsoffice

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


def test_turtle_file():
    dump()
    result = turtle(filename=f"tests/ttl/{model_name}.ttl")
    print(result)
    return result


if __name__ == "__main__":
    bldg = test_create_a_building()
    result = test_turtle_file()
    print(f"Check file : tests/ttl/{model_name}.ttl")
    print(result)
    graph = get_datagraph()  # this is there to be used with python -i option
