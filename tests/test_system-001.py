from pathlib import Path

from header import ttl_test_header

from bob import core
from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.core import (
    Device,
    InletSystemConnectionPoint,
    OutletSystemConnectionPoint,
    System,
    bind_model_namespace,
    dump,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")
core.INCLUDE_INVERSE = True


def test_systems(bob_fixture):
    class A(Device):
        cOut: AirOutletConnectionPoint

    class X(System):
        cOut: OutletSystemConnectionPoint

    class B(Device):
        cIn: AirInletConnectionPoint

    class Y(System):
        cIn: InletSystemConnectionPoint

    a = A(label="a")
    x = X(label="x")
    x.cOut.mapsTo = a.cOut

    b = B(label="b")
    y = Y(label="y")
    y.cIn.mapsTo = b.cIn

    # one system connection point to another
    x.cOut >> y.cIn

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
