from pathlib import Path

from header import sample_header

from bob.connections.air import (
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from bob.connections.water import (
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from bob.core import (
    Device,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    System,
    SystemConnectionPoint,
    bind_model_namespace,
    dump,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# make a couple devices
d1 = Device(label="d1")
d2 = Device(label="d2")

# create some connection points on the fly
d1_cp = AirOutletConnectionPoint(d1, label="d1.cp")
d2_cp = AirInletConnectionPoint(d2, label="d2.cp")

# make a couple systems
s1 = System(label="s1")
s2 = System(label="s2")

# create some bi-directional connection points on the fly
s1_cp = AirOutletSystemConnectionPoint(s1, label="s1.cp", mapsTo=d1_cp)
s2_cp = AirInletSystemConnectionPoint(s2, label="s2.cp", mapsTo=d2_cp)

# connect the connection points together (directional connection)
s1_cp >> s2_cp

# make a couple devices
d3 = Device(label="d3")
d4 = Device(label="d4")

# create some connection points on the fly
d3_cp = WaterOutletConnectionPoint(d3, label="d3.cp")
d4_cp = WaterInletConnectionPoint(d4, label="d4.cp")

# make a couple systems
s3 = System(label="s3")
s4 = System(label="s4")

# create some directional connection points on the fly
s3_ocp = OutletSystemConnectionPoint(s3, label="s3.ocp", mapsTo=d3_cp)
s4_icp = InletSystemConnectionPoint(s4, label="s4.icp", mapsTo=d4_cp)

# connect the systems together
s3 >> s4

# dump the result
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
