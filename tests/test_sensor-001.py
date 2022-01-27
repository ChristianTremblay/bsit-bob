from bob.core import bind_model_namespace, dump, turtle, get_datagraph
from bob.sensor.temperature import AirTemperatureSensor
from bob.sensor.humidity import AirHumiditySensor
import pytest

__namespace__ = bind_model_namespace("ex", "urn:ex/")


# def test_fail_to_create_air_temp_sensor():
#    with pytest.raises(ValueError):
#        ats = AirTemperatureSensor(
#            label="DA-T",
#            comment="Supply Air Temperature Sensor",
#            extref="bacnet://570005/analog-input,10084/present-value",
#        )


def test_create_air_temp_sensor():
    ats = AirTemperatureSensor(
        label="DA-T",
        comment="Supply Air Temperature Sensor",
        extref=["bacnet://570005/analog-input,10084/present-value"],
    )
    return ats


def test_create_air_humidity_sensor_with_value():
    ahs = AirHumiditySensor(
        label="ZN-H", comment="Zone Humidity Sensor with a value of 20", value=20
    )
    return ahs


def test_create_air_humidity_sensor():
    ahs = AirHumiditySensor(
        label="ZN-H",
        comment="Zone Humidity Sensor with a BACnet reference and a Niagara4 ORD",
        extref=[
            "bacnet://570005/analog-input,10085/present-value",
            "ip:172.16.3.8|foxs:|station:|slot:/Drivers/BacnetNetwork/MSTP70/PCA$2d70$2d005_SystemeUV1/points/ZN$2dH",
        ],
    )
    return ahs


def test_turtle_file():
    dump()
    result = turtle()
    print(result)


if __name__ == "__main__":
    ats = test_create_air_temp_sensor()
    ahs_val = test_create_air_humidity_sensor_with_value()
    ahs = test_create_air_humidity_sensor()
    result = turtle()
    with open("test_sensor-001_results.ttl", "w") as file:
        file.write(result)
    print("Check file : test_sensor-001_results.ttl")
    print(result)
    graph = get_datagraph()
