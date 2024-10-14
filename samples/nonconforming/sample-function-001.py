"""
Sample function with one input and one output associated with properties
after creation.
"""

from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.core import EX, Property, bind_model_namespace, dump
from bob.producer import Function, G36AnalogInput, G36AnalogOutput
from bob.scratch.header import sample_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class Sample(Function):
    x: G36AnalogInput
    y: G36AnalogOutput

    def eval(self):
        self.y = self.x * 10 + 12


xp = Property(1.2, label="x")
yp = Property(3.4, label="y")

f = Sample(label="f", x=xp, y=yp)

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
