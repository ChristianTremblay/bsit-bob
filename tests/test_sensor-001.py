from bob.core import bind_model_namespace, dump, enum
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
        measuresSubstance=enum["Medium-Air"],
        hasExternalReference=["bacnet://570005/analog-input,10084/present-value"],
    )

    ats2 = AirTemperatureSensor(
        label="ats2",
        comment="Supply Air Temperature Sensor",
        hasExternalReference=["bacnet://570005/analog-input,10084/present-value"],
    )

    ahs1 = AirHumiditySensor(
        label="ahs1", comment="Zone Humidity Sensor with a value of 20", hasValue=20
    )

    ahs2 = AirHumiditySensor(
        label="ahs2",
        comment="Zone Humidity Sensor with a BACnet reference and a Niagara4 ORD",
        hasExternalReference=[
            "bacnet://570005/analog-input,10085/present-value",
            "ip:172.16.3.8|foxs:|station:|slot:/Drivers/BacnetNetwork/MSTP70/PCA$2d70$2d005_SystemeUV1/points/ZN$2dH",
        ],
    )

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
