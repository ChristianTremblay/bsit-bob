from bob.core import bind_model_namespace, dump
from bob.core import Junction, Device, ConnectionPoint

__namespace__ = bind_model_namespace("ex", "urn:ex/")

d1 = Device(label="d1")
cp1 = ConnectionPoint(d1)

j1 = Junction()
cp1.link_to(j1)

dump()
