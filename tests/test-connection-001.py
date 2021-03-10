from bob.core import bind_model_namespace, Device, ConnectionPoint, Connection, dump

__namespace__ = bind_model_namespace("ex", "urn:ex/")

d1 = Device(label="d1")
cp1 = ConnectionPoint(d1)

c = Connection()
c.connect_to(cp1)

dump()
