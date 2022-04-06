from pathlib import Path

from header import sample_header

from bob.core import DomainSpace, PhysicalSpace, bind_model_namespace, dump

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


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

room_101_hvac = DomainSpace(label="building.1fl.hvac")
room_101_hvac < room_101

room_101_lighting = DomainSpace(label="building.1fl.lighting")
room_101_lighting < room_101

# dump the result
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
