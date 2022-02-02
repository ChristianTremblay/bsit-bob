from bob.core import (
    bind_model_namespace,
    dump,
    turtle,
    ExternalReference,
    get_datagraph,
    Value,
    quantitykind,
    unit,
    enum,
    Device,
)

from bob.devices.hvac import Fan

__namespace__ = bind_model_namespace("ex", "urn:ex/")


def test_create_fan():
    _config = {
        "params": {"label": "VA-1", "comment": "Supply Fan"},
        "sensors": {},
        "contains": {("VA1-VFD", Device): {"comment": "VFD for VA-1"}},
    }
    fan = Fan(
        config=_config,
    )

    return fan


def test_create_fan_no_config():
    fan = Fan(
        label="VA-2",
    )

    return fan


def test_turtle_file():
    dump()
    result = turtle()
    print(result)


if __name__ == "__main__":
    fan = test_create_fan()
    fan2 = test_create_fan_no_config()
    result = turtle()
    with open("test_device-005_results.ttl", "w") as file:
        file.write(result)
    print("Check file : test_device-005_results.ttl")
    print(result)
    graph = get_datagraph()
