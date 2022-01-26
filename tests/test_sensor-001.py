from bob.core import bind_model_namespace, dump, turtle
from bob.sensor.temperature import AirTemperatureSensor

__namespace__ = bind_model_namespace("ex", "urn:ex/")


def test_create_air_temp_sensor():
    ats = AirTemperatureSensor(
        label="DA-T",
        comment="Supply Air Temperature Sensor",
        datasource="bacnet://570005/analog-input,10084/present-value",
    )


def test_turtle_file():
    dump()
    result = turtle()
    print(result)


if __name__ == "__main__":
    test_create_air_temp_sensor()
    result = turtle()
    with open("test_sensor-001_results.ttl", "w") as file:
        file.write(result)
    print("Check file : test_sensor-001_results.ttl")
    print(result)
