from bob.core import (
    bind_model_namespace,
    Junction,
    Segment,
    Device,
    ConnectionPoint,
    dump,
)

__namespace__ = bind_model_namespace("ex", "urn:ex/")

d1 = Device(label="d1")
cp1 = ConnectionPoint(d1)

d2 = Device(label="d2")
cp2 = ConnectionPoint(d2)

j1 = Junction()
j1.link_to(cp1)
j1.link_to(cp2)

dump()
