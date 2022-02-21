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

from pathlib import Path

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


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
    result = turtle(filename=f"tests/ttl/{model_name}.ttl")
    print(result)
    return result


if __name__ == "__main__":
    fan = test_create_fan()
    fan2 = test_create_fan_no_config()
    result = test_turtle_file()
    print(f"Check file : tests/ttl/{model_name}.ttl")
    print(result)
    graph = get_datagraph()  # this is there to be used with python -i option
