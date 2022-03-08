from bob.core import bind_model_namespace, dump, Air, Medium
from bob.sensor.temperature import AirTemperatureSensor, TemperatureSensor
from bob.sensor.humidity import AirHumiditySensor
import pytest

from pathlib import Path
from header import ttl_test_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_sensor():
    with pytest.raises(ValueError):
        ats = TemperatureSensor(
            label="DA-T",
            comment="Supply Air Temperature Sensor",
            hasExternalReference=["bacnet://570005/analog-input,10084/present-value"],
        )

    ats1 = TemperatureSensor(
        label="ats1",
        comment="Supply Air Temperature Sensor",
        measuresMedium=Air
        # hasExternalReference=["bacnet://570005/analog-input,10084/present-value"],
    )

    ats2 = AirTemperatureSensor(
        label="ats2",
        comment="Supply Air Temperature Sensor",
        hasExternalReference=["bacnet://570005/analog-input,10084/present-value"],
    )

    ahs1 = AirHumiditySensor(
        label="ahs1", comment="Zone Humidity Sensor with a value of 20", hasValue=20
    )


ats1 = TemperatureSensor(
    label="ats1",
    comment="Supply Air Temperature Sensor",
    measuresMedium=Air,
    hasExternalReference=["bacnet://570005/analog-input,10084/present-value"],
)

dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
