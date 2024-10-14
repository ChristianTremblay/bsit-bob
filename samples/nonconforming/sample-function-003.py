"""
Function with a single parameter with the value provided to `__init__()`.
"""

from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.core import EX, Property, bind_model_namespace, dump
from bob.producer import Function, FunctionInput
from bob.scratch.header import sample_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class Sample(Function):
    offset: FunctionInput


f = Sample(label="f", offset=5.6)

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
