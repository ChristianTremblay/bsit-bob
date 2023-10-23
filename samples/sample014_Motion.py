from pathlib import Path

from header import sample_header

from bob.core import DomainSpace, PhysicalSpace, bind_model_namespace, dump
from bob.property import EnumeratedObservableProperty, QuantifiableObservableProperty

from bob.enum import HVAC
from bob.space.hvac import HVACSpace
from bob.sensor.motion import OccupantCounterSensor, OccupantMotionSensor

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")

space = HVACSpace(label="Room 101")

ms = OccupantMotionSensor(hasObservationLocation=space, label="Motion Sensor")
pc = OccupantCounterSensor(hasObservationLocation=space, label="People Counter")


dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
