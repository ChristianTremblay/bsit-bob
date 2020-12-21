from bob.core import (
    bind_model_namespace,
    System,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    dump,
    clear,
)

from samples import sample_header

# instances will come from this namespace, otherwise they would be BNode's
bind_model_namespace("ex", "urn:ex/")

# make a couple systems
s1 = System(label="s1")
s2 = System(label="s2")

# create some bi-directional connection points on the fly
s1_cp = ConnectionPoint(s1, label="s1.cp")
s2_cp = ConnectionPoint(s2, label="s2.cp")

# connect the connection points together (directional connection)
s1_cp >> s2_cp

# make a couple systems
s3 = System(label="s3")
s4 = System(label="s4")

# create some directional connection points on the fly
s3_ocp = OutletConnectionPoint(s3, label="s3.ocp")
s4_icp = InletConnectionPoint(s4, label="s4.icp")

# connect the systems together
s3 >> s4

# dump the result
sample_header("sample010")
dump()
