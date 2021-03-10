import sys
from bob.core import *

__namespace__ = bind_model_namespace("ex", "urn:ex/")


class A(Device):
    cOut: OutletConnectionPoint


class X(System):
    cOut: SystemOutletConnectionPoint


class B(Device):
    cIn: InletConnectionPoint


class Y(System):
    cIn: SystemInletConnectionPoint


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
