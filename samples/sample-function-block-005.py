"""
Function with a single constant with the value provided in the class definition
and overridden in `__init__()`.
"""
from pathlib import Path

from header import sample_header

from bob.core import EX, Property, bind_model_namespace, dump
from bob.functions import Constant, FunctionBlock

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class Sample(FunctionBlock):
    offset: Constant = 1.2


f = Sample(label="f", offset=3.4)

# dump the result
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
