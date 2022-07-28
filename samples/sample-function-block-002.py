"""
Sample function with one input and one output associated with properties
provided to `__init__()`.
"""
from pathlib import Path

from header import sample_header

from bob.core import bind_model_namespace, dump, EX, Property
from bob.functions import FunctionBlock, AnalogInput, AnalogOutput

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class Sample(FunctionBlock):
    x: AnalogInput
    y: AnalogOutput


xp = Property(1.2, label="x")
yp = Property(3.4, label="y")

f = Sample(label="f", x=xp, y=yp)

# dump the result
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
