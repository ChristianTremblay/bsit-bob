from pathlib import Path

from bob.core import UNIT, bind_model_namespace, dump
from bob.properties.physical import Area
from bob.space.physical import Bathroom, Building, Corridor, Floor, Office, Roof, Room

model_name = Path(__file__).stem
global_ns = Path(__file__).parent.stem
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}/{model_name}/")


# Define the building Physical Spaces
bldg = Building(
    label="Pritoni Building",
    Area=Area(1060, hasUnit=UNIT.FT2, label="Pritoni Building.Area"),
)
roof = Roof(label="Roof of building")
floor1 = Floor(label="Floor1")
openoffice = Office(
    label="Open office", Area=Area(600, hasUnit=UNIT.FT2, label="Open office.Area")
)
bathroom = Bathroom(
    label="Bathroom", Area=Area(75, hasUnit=UNIT.FT2, label="Bathroom.Area")
)
private_office = Office(
    label="Private office", Area=Area(150, hasUnit=UNIT.FT2, label="Private office.Area")
)
kitchenette = Room(
    label="Kitchenette", Area=Area(120, hasUnit=UNIT.FT2, label="Kitchenette.Area")
)
corridor = Corridor(
    label="Corridor", Area=Area(115, hasUnit=UNIT.FT2, label="Corridor.Area")
)

if __name__ == "__main__":
    dump()
