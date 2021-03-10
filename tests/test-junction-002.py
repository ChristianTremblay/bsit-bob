from bob.core import (
    bind_model_namespace,
    Junction,
    Segment,
    Device,
    ConnectionPoint,
    dump,
)

__namespace__ = bind_model_namespace("ex", "urn:ex/")

j1 = Junction()
j2 = Junction()
j1.link_to(j2)

dump()
