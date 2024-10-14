"""
g36_4-1_VAV_TerminalUnit_CoolingOnly
"""

from __future__ import annotations

from pathlib import Path

from header import g36_header

from bob.assemblage import create_data_and_schema_ttl
from bob.core import bind_model_namespace, dump
from bob.producer.g36 import G36VAVCoolingOnly
from bob.scratch.header import sample_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace(
    "exg3601", f"http://data.ashrae.org/standard223/data/{model_name}#"
)

g36VAVcoolingOnly = G36VAVCoolingOnly(label="Simplest implementation")
_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
