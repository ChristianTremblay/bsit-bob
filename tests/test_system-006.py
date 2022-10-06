from pathlib import Path

from header import ttl_test_header

from bob import core
from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.core import (
    Air,
    Connection,
    Equipment,
    InletSystemConnectionPoint,
    OutletSystemConnectionPoint,
    System,
    bind_model_namespace,
    dump,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")
core.INCLUDE_INVERSE = True


def test_systems_006(bob_fixture):
    class A(Equipment):
        cOut: AirOutletConnectionPoint

    class X(System):
        cOut: OutletSystemConnectionPoint

    class B(Equipment):
        cIn: AirInletConnectionPoint

    class Y(System):
        cIn: InletSystemConnectionPoint

    a = A(label="a")
    x = X(label="x")
    x.cOut.mapsTo = a.cOut

    b = B(label="b")
    y = Y(label="y")
    y.cIn.mapsTo = b.cIn

    # connection from system connection point
    c = Connection(hasMedium=Air)
    c << x.cOut

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
