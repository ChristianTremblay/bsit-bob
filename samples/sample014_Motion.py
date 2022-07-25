from pathlib import Path

from header import sample_header

from bob.core import DomainSpace, PhysicalSpace, bind_model_namespace, dump
from bob.enum import HVAC
from bob.sensor.motion import MotionSensor, PeopleCounter

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# make a building with some floors and rooms

ms = MotionSensor(label="Motion Sensor")
pc = PeopleCounter(label="People Counter")

dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
