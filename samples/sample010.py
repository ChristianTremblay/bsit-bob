from pathlib import Path

from bob.core import (
    bind_model_namespace,
    System,
    SystemConnectionPoint,
    SystemInletConnectionPoint,
    SystemOutletConnectionPoint,
    dump,
    clear,
)

from header import sample_header


model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# make a couple systems
s1 = System(label="s1")
s2 = System(label="s2")

# create some bi-directional connection points on the fly
s1_cp = SystemConnectionPoint(s1, label="s1.cp")
s2_cp = SystemConnectionPoint(s2, label="s2.cp")

# connect the connection points together (directional connection)
s1_cp >> s2_cp

# make a couple systems
s3 = System(label="s3")
s4 = System(label="s4")

# create some directional connection points on the fly
s3_ocp = SystemOutletConnectionPoint(s3, label="s3.ocp")
s4_icp = SystemInletConnectionPoint(s4, label="s4.icp")

# connect the systems together
s3 >> s4

# dump the result
sample_header(model_name)
dump()
