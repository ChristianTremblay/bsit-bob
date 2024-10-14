from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.core import (
    DomainSpace,
    PhysicalSpace,
    bind_model_namespace,
    data_graph,
    dump,
    schema_graph,
)
from bob.enum import HVAC
from bob.scratch.header import sample_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# make a building with some floors and rooms
building = PhysicalSpace(label="building")

first_floor = PhysicalSpace(label="building.1fl")
room_101 = PhysicalSpace(label="building.rm101")
room_102 = PhysicalSpace(label="building.rm102")

second_floor = PhysicalSpace(label="building.2fl")
room_201 = PhysicalSpace(label="building.rm201")
room_202 = PhysicalSpace(label="building.rm202")

building > first_floor
first_floor > room_101
first_floor > room_102

building > second_floor
second_floor > room_201
second_floor > room_202

room_101_hvac = DomainSpace(label="building.1fl.hvac", hasDomain=HVAC)
room_101_hvac < room_101

room_101_lighting = DomainSpace(label="building.1fl.lighting", hasDomain=HVAC)
room_101_lighting < room_101

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
