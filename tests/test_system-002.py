from bob import core
from bob.core import (
    bind_model_namespace,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    Device,
    System,
    dump,
)
from pathlib import Path
from header import ttl_test_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")
core.INCLUDE_INVERSE = True


def test_systems_002():
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

    # one system connection point from another
    y.cIn << x.cOut

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
