"""
Function with a single constant with the value provided in the class definition
and overridden in `__init__()`.
"""

from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.core import EX, Property, bind_model_namespace, dump
from bob.producer import Function, FunctionInput
from bob.scratch.header import sample_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class Sample(Function):
    offset: FunctionInput = 1.2


f = Sample(label="f", offset=4.5)

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
