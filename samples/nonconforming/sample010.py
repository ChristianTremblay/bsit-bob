from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.connections.liquid import WaterInletConnectionPoint, WaterOutletConnectionPoint
from bob.core import (
    Equipment,
    System,
    bind_model_namespace,
    data_graph,
    dump,
    schema_graph,
)
from bob.scratch.header import sample_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# make a couple Equipment
d1 = Equipment(label="d1")
d2 = Equipment(label="d2")

# create some connection points on the fly
d1_cp = AirOutletConnectionPoint(d1, label="d1.cp")
d2_cp = AirInletConnectionPoint(d2, label="d2.cp")

# make a couple systems
s1 = System(label="s1")
s2 = System(label="s2")

# create some bi-directional connection points on the fly
s1.add_boundary_connection_point(d1_cp)
s2.add_boundary_connection_point(d2_cp)

# connect the connection points together (directional connection)
s1 >> s2

# make a couple Equipment
d3 = Equipment(label="d3")
d4 = Equipment(label="d4")

# create some connection points on the fly
d3_cp = WaterOutletConnectionPoint(d3, label="d3.cp")
d4_cp = WaterInletConnectionPoint(d4, label="d4.cp")

# make a couple systems
s3 = System(label="s3")
s4 = System(label="s4")

# create some directional connection points on the fly
s3.add_boundary_connection_point(d3_cp)
s4.add_boundary_connection_point(d4_cp)

# connect the systems together
s3 >> s4

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
