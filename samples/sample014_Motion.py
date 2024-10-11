from pathlib import Path

from bob.core import (
    bind_model_namespace,
    data_graph,
    schema_graph,
    dump,
    EnumeratedObservableProperty,
    QuantifiableObservableProperty,
    DomainSpace,
    PhysicalSpace,
)
from bob.scratch.header import sample_header

from bob.enum import HVAC
from bob.space.hvac import HVACSpace
from bob.sensor.motion import OccupantCounterSensor, OccupantMotionSensor

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")

space = HVACSpace(label="Room 101")

ms = OccupantMotionSensor(hasObservationLocation=space, label="Motion Sensor")
pc = OccupantCounterSensor(hasObservationLocation=space, label="People Counter")

# dump the result
dump(
    data_graph,
    filename=f"samples/ttl/{model_name}.data.ttl",
    header=sample_header(model_name),
)
dump(schema_graph, filename=f"samples/ttl/{model_name}.schema.ttl")
