from pathlib import Path

from bob.core import (
    DomainSpace,
    Zone,
    bind_model_namespace,
    dump,
    turtle,
    ExternalReference,
    get_datagraph,
)
from bob.connections import (
    AirInletConnectionPoint,
    AirInletZoneConnectionPoint,
    ChilledWaterConnection,
)

from bob.devices.hvac import Fan, ChilledWaterCoil

# from header import sample_header


model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_connect_devices_and_map_zone():
    # there is a chilled water connection, we don't know where the chilled
    # is coming from
    c = ChilledWaterConnection()

    # there is a chilled water coil (itself a system) that is a subsystem
    # of a larger context
    coil1 = ChilledWaterCoil(label="CW-Coil-1")

    # the coil gets its chilled water from the connection
    c >> coil1

    # there is a fan, and the air output of the fan goes into the coil
    f = Fan(label="F")
    f >> coil1


def test_turtle_file():
    dump()
    result = turtle(filename=f"tests/ttl/{model_name}.ttl")
    print(result)
    return result


if __name__ == "__main__":
    pm = test_connect_devices_and_map_zone()
    result = test_turtle_file()
    print(f"Check file : tests/ttl/{model_name}.ttl")
    print(result)
    graph = get_datagraph()  # this is there to be used with python -i option
