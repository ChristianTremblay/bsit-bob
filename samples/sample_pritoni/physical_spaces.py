from pathlib import Path

from bob.core import bind_model_namespace, dump
from bob.space.physical import Bathroom, Building, Corridor, Floor, Office, Roof, Room

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")


# Define the building Physical Spaces
bldg = Building(label="Pritoni Building")
roof = Roof(label="Roof of building")
floor1 = Floor(label="Floor1")
openoffice = Office(label="Open office")
bathroom = Bathroom(label="Bathroom")
private_office = Office(label="Private office")
kitchenette = Room(label="Kitchenette")
corridor = Corridor(label="Corridor")

if __name__ == "__main__":
    dump()
