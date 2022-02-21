from bob.core import bind_model_namespace, dump, turtle, get_datagraph, enum
from bob.sensor.temperature import AirTemperatureSensor, TemperatureSensor
from bob.sensor.humidity import AirHumiditySensor
import pytest

from pathlib import Path

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# def test_fail_to_create_air_temp_sensor():
#    with pytest.raises(ValueError):
#        ats = AirTemperatureSensor(
#            label="DA-T",
#            comment="Supply Air Temperature Sensor",
#            extref="bacnet://570005/analog-input,10084/present-value",
#        )


def test_create_air_temp_sensor_MissingMeasureSubstance():
    with pytest.raises(ValueError):
        ats = TemperatureSensor(
            label="DA-T",
            comment="Supply Air Temperature Sensor",
            hasExternalReference=["bacnet://570005/analog-input,10084/present-value"],
        )
        return ats


def test_create_air_temp_sensor_1():
    ats = TemperatureSensor(
        label="DA-T",
        comment="Supply Air Temperature Sensor",
        measuresSubstance=enum["Medium-Air"],
        hasExternalReference=["bacnet://570005/analog-input,10084/present-value"],
    )
    return ats


def test_create_air_temp_sensor_2():
    ats = AirTemperatureSensor(
        label="DA-T",
        comment="Supply Air Temperature Sensor",
        hasExternalReference=["bacnet://570005/analog-input,10084/present-value"],
    )
    return ats


def test_create_air_humidity_sensor_with_value():
    ahs = AirHumiditySensor(
        label="ZN-H", comment="Zone Humidity Sensor with a value of 20", hasValue=20
    )
    return ahs


def test_create_air_humidity_sensor():
    ahs = AirHumiditySensor(
        label="ZN-H",
        comment="Zone Humidity Sensor with a BACnet reference and a Niagara4 ORD",
        hasExternalReference=[
            "bacnet://570005/analog-input,10085/present-value",
            "ip:172.16.3.8|foxs:|station:|slot:/Drivers/BacnetNetwork/MSTP70/PCA$2d70$2d005_SystemeUV1/points/ZN$2dH",
        ],
    )
    return ahs


def test_turtle_file():
    dump()
    result = turtle(filename=f"tests/ttl/{model_name}.ttl")
    print(result)
    return result


if __name__ == "__main__":
    ats = test_create_air_temp_sensor_2()
    ahs_val = test_create_air_humidity_sensor_with_value()
    ahs = test_create_air_humidity_sensor()
    # panel2 = test_create_emptyelectricalpaneldevice()
    result = test_turtle_file()
    print(f"Check file : tests/ttl/{model_name}.ttl")
    print(result)
    graph = get_datagraph()  # this is there to be used with python -i option
