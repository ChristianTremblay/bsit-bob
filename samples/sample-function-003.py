"""
Function with a single parameter with the value provided to `__init__()`.
"""

from pathlib import Path

from bob.core import EX, Property, bind_model_namespace, dump
from bob.producer import Function, FunctionInput
from bob.scratch.header import sample_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class Sample(Function):
    offset: FunctionInput


f = Sample(label="f", offset=5.6)

# dump the result
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
