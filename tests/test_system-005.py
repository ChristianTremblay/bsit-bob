from bob.core import (
    bind_model_namespace,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    Device,
    System,
    Connection,
    dump,
)
from bob import core

__namespace__ = bind_model_namespace("ex", "urn:ex/")
core.INCLUDE_INVERSE = True


class A(Device):
    cOut: OutletConnectionPoint


class X(System):
    cOut: OutletSystemConnectionPoint


class B(Device):
    cIn: InletConnectionPoint


class Y(System):
    cIn: InletSystemConnectionPoint


a = A(label="a")
x = X(label="x")
x.cOut.mapsTo = a.cOut

b = B(label="b")
y = Y(label="y")
y.cIn.mapsTo = b.cIn

# connection to system connection point
c = Connection()
c >> y.cIn

dump()
