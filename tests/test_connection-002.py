from bob.core import bind_model_namespace, dump
from bob.core import Device, ConnectionPoint, Connection
from bob import core

__namespace__ = bind_model_namespace("ex", "urn:ex/")
core.INCLUDE_INVERSE = True

d1 = Device(label="d1")
cp1 = ConnectionPoint(d1)

c = Connection()
c.connect_from(cp1)

dump()
