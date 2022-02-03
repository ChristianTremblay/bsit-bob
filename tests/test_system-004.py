import sys
from bob.core import bind_model_namespace, dump, turtle
from bob.core import (
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    Device,
    System,
)
from bob import core

__namespace__ = bind_model_namespace("ex", "urn:ex/")
core.EXPLICIT_RECIPROCITY = True


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

# system from system
y << x
dump()
result = turtle()


def test_result():
    print(result)
