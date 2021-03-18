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

s1 = Segment()
cp1.link_to(s1)

dump()
