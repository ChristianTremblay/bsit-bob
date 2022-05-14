from pathlib import Path

from header import ttl_test_header

from bob.core import bind_model_namespace, dump
from bob.devices.hvac.particlecounter import ParticleCounter
from bob.sensor.particle import (
    CoarseParticulateSensor,
    FineParticulateSensor,
    UltraFineParticulateSensor,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_particle_counter(bob_fixture):
    particlecounter_config = {
        "properties": {},
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
        },
    }

    pm = ParticleCounter(
        label="PM-1",
        comment="Particulate Measurement Station AKA particle counter",
        config=particlecounter_config,
    )

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
