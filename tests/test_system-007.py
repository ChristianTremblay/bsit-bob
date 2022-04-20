from pathlib import Path

from header import ttl_test_header

from bob import core
from bob.core import (
    Connection,
    Device,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    System,
    bind_model_namespace,
    dump,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")
core.INCLUDE_INVERSE = True


def test_systems_007(bob_fixture):
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

    # connection from and to a system connection point, chained
    c = Connection()
    x.cOut >> c >> y.cIn

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
