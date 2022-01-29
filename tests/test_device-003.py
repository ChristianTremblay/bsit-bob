from bob.core import (
    bind_model_namespace,
    dump,
    turtle,
    ExternalReference,
    get_datagraph,
)

from bob.devices.hvac.particlecounter import ParticleCounter

__namespace__ = bind_model_namespace("ex", "urn:ex/")


def test_create_particulatemeasuredevice():
    pm = ParticleCounter(
        label="PM-1",
        comment="Particulate Measurement Station AKA particle counter",
        coarse_extref="bacnet://1/analog-value,1/present-value",
        fine_extref="bacnet://1/analog-input,2/present-value",
        ultrafine_extref="bacnet://1/analog-input,3/present-value",
    )

    return pm


def test_turtle_file():
    dump()
    result = turtle()
    print(result)


if __name__ == "__main__":
    pm = test_create_particulatemeasuredevice()
    result = turtle()
    with open("test_sensor-003_results.ttl", "w") as file:
        file.write(result)
    print("Check file : test_sensor-003_results.ttl")
    print(result)
    graph = get_datagraph()
