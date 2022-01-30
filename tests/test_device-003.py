from bob.core import (
    bind_model_namespace,
    dump,
    turtle,
    ExternalReference,
    get_datagraph,
)

from bob.devices.hvac.particlecounter import ParticleCounter
from bob.sensor.particle import (
    CoarseParticulateSensor,
    FineParticulateSensor,
    UltraFineParticulateSensor,
)

__namespace__ = bind_model_namespace("ex", "urn:ex/")

particlecounter_config = {
    "sensors": {
        ("coarse_sensor", CoarseParticulateSensor): {
            "hasExternalReference": "bacnet://1/analog-value,1/present-value",
        },
        ("fine_sensor", FineParticulateSensor): {
            "hasExternalReference": "bacnet://1/analog-input,2/present-value",
        },
        ("ultrafine_sensor", UltraFineParticulateSensor): {
            "hasExternalReference": "bacnet://1/analog-input,3/present-value",
        },
    }
}


def test_create_particulatemeasuredevice():
    pm = ParticleCounter(
        label="PM-1",
        comment="Particulate Measurement Station AKA particle counter",
        config=particlecounter_config,
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
