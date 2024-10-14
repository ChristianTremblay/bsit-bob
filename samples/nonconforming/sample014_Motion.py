from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.core import (
    DomainSpace,
    EnumeratedObservableProperty,
    PhysicalSpace,
    QuantifiableObservableProperty,
    bind_model_namespace,
    data_graph,
    dump,
    schema_graph,
)
from bob.enum import HVAC
from bob.scratch.header import sample_header
from bob.sensor.motion import OccupantCounterSensor, OccupantMotionSensor
from bob.space.hvac import HVACSpace

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")

space = HVACSpace(label="Room 101")

ms = OccupantMotionSensor(hasObservationLocation=space, label="Motion Sensor")
pc = OccupantCounterSensor(hasObservationLocation=space, label="People Counter")

# dump the result
_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
