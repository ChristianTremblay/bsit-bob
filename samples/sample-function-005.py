"""
Function with a single constant with the value provided in the class definition
and overridden in `__init__()`.
"""

from pathlib import Path

from bob.core import EX, Property, bind_model_namespace, dump
from bob.producer import Function, FunctionInput
from bob.scratch.header import sample_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class Sample(Function):
    offset: FunctionInput = 1.2


f = Sample(label="f", offset=4.5)

# dump the result
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
