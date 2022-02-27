import pytest
from bob.core import (
    bind_model_namespace,
    Device,
    Connection,
    InletConnectionPoint,
    OutletConnectionPoint,
    dump,
)

__namespace__ = bind_model_namespace("ex", "urn:ex/")

d1 = Device(label="d1")
cp1 = OutletConnectionPoint(d1, label="d1.out")

d2 = Device(label="d2")
cp2 = InletConnectionPoint(d2, label="d2.in")

c = Connection()

with pytest.raises(TypeError):
    c.connect_to(cp1)

with pytest.raises(TypeError):
    c.connect_from(cp2)

dump()
