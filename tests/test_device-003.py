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

from pathlib import Path

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")

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
    result = turtle(filename=f"tests/ttl/{model_name}.ttl")
    print(result)
    return result


if __name__ == "__main__":
    pm = test_create_particulatemeasuredevice()
    result = test_turtle_file()
    print(f"Check file : tests/ttl/{model_name}.ttl")
    print(result)
    graph = get_datagraph()  # this is there to be used with python -i option
