"""
Function with a single parameter with the value provided in the class
definition.
"""
from pathlib import Path

from header import sample_header

from bob.core import EX, Property, bind_model_namespace, dump
from bob.producer import FunctionBlock, Parameter

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class Sample(FunctionBlock):
    offset: Parameter = 7.8


f = Sample(label="f")

# dump the result
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
