from bob.core import bind_model_namespace, dump, turtle
from bob.sensor.temperature import AirTemperatureSensor
from bob.sensor.humidity import AirHumiditySensor

__namespace__ = bind_model_namespace("ex", "urn:ex/")


def test_create_air_temp_sensor():
    ats = AirTemperatureSensor(
        label="DA-T",
        comment="Supply Air Temperature Sensor",
        datasource="bacnet://570005/analog-input,10084/present-value",
    )


def test_create_air_humidity_sensor():
    ats = AirHumiditySensor(
        label="ZN-H",
        comment="Zone Humidity Sensor",
        datasource="bacnet://570005/analog-input,10085/present-value",
    )


def test_turtle_file():
    dump()
    result = turtle()
    print(result)


if __name__ == "__main__":
    test_create_air_temp_sensor()
    test_create_air_humidity_sensor()
    result = turtle()
    with open("test_sensor-001_results.ttl", "w") as file:
        file.write(result)
    print("Check file : test_sensor-001_results.ttl")
    print(result)
