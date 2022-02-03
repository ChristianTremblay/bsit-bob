from bob.core import (
    bind_model_namespace,
    dump,
    turtle,
    ExternalReference,
    get_datagraph,
    Value,
    quantitykind,
    unit,
    enum,
    quantityValue,
)

from bob.devices.hvac.gas import GasMonitor
from bob.property import QuantifiableObservableProperty
from bob.sensor.gas import CO2Sensor, NO2Sensor, COSensor
from bob.sensor.temperature import AirTemperatureSensor

__namespace__ = bind_model_namespace("ex", "urn:ex/")


def test_create_gasmonitordevice():
    dual_no2_co_configuration_example = {
        "sensors": {
            ("CO_sensor", COSensor): {
                "hasExternalReference": "bacnet://",
                "hasMinRange": QuantifiableObservableProperty(
                    0,
                    hasQuantityKind=quantitykind.DimensionlessRatio,
                    unit=unit.PPM,
                    label="CO_sensor.MinRange",
                ),
                "hasMaxRange": QuantifiableObservableProperty(
                    100,
                    hasQuantityKind=quantitykind.DimensionlessRatio,
                    unit=unit.PPM,
                    label="CO_sensor.MaxRange",
                ),
            },
            ("NO2_sensor", NO2Sensor): {
                "hasExternalReference": "bacnet://",
                "hasMinRange": QuantifiableObservableProperty(
                    0,
                    hasQuantityKind=quantitykind.DimensionlessRatio,
                    unit=unit.PPM,
                    label="NO2_sensor.MinRange",
                ),
                "hasMaxRange": QuantifiableObservableProperty(
                    250,
                    hasQuantityKind=quantitykind.DimensionlessRatio,
                    unit=unit.PPM,
                    label="NO2_sensor.MaxRange",
                ),
            },
        }
    }
    dualgasmonitor = GasMonitor(
        label="GM-1",
        comment="Dual Gas Monitoring Device that measure NO2 and CO. Usually used in underground parking lot",
        config=dual_no2_co_configuration_example,
    )

    return dualgasmonitor


def test_create_co2monitordevice():
    _config = {
        "sensors": {
            ("CO2_sensor", CO2Sensor): {
                "hasExternalReference": "bacnet://",
                "hasMinRange": QuantifiableObservableProperty(
                    0,
                    hasQuantityKind=quantitykind.DimensionlessRatio,
                    unit=unit.PPM,
                    label="CO2_sensor.inRange",
                ),
                "hasMaxRange": QuantifiableObservableProperty(
                    2000,
                    hasQuantityKind=quantitykind.DimensionlessRatio,
                    unit=unit.PPM,
                    label="CO2_sensor.MaxRange",
                ),
            },
        }
    }
    co2monitor = GasMonitor(
        label="CO2-1",
        comment="CO2 Monitor",
        config=_config,
    )

    return co2monitor


def test_create_co2monitordevice_with_temperature():
    _config = {
        "params": {
            "label": "CO2-2",
            "comment": "CO2 Monitor with temperature reading",
        },
        "sensors": {
            ("CO2_sensor", CO2Sensor): {
                "hasExternalReference": "bacnet://",
                "hasMinRange": QuantifiableObservableProperty(
                    0,
                    hasQuantityKind=quantitykind.DimensionlessRatio,
                    unit=unit.PPM,
                    label="CO2_sensor.MinRange",
                ),
                "hasMaxRange": QuantifiableObservableProperty(
                    2000,
                    hasQuantityKind=quantitykind.DimensionlessRatio,
                    unit=unit.PPM,
                    label="CO2_sensor.MaxRange",
                ),
            },
            ("Temperature_sensor", AirTemperatureSensor): {
                # "measuresSubstance": enum["Medium-Air"],
                "hasExternalReference": "bacnet://",
                "hasMinRange": QuantifiableObservableProperty(
                    0,
                    hasQuantityKind=quantitykind.Temperature,
                    unit=unit.DEG_C,
                    label="Temperature_sensor.MinRange",
                ),
                "hasMaxRange": QuantifiableObservableProperty(
                    50,
                    hasQuantityKind=quantitykind.Temperature,
                    unit=unit.DEG_C,
                    label="Temperature_sensor.MaxRange",
                ),
                "comment": "Internal temperature sensor of device",
            },
        },
    }
    co2monitor = GasMonitor(
        config=_config,
    )

    return co2monitor


def test_turtle_file():
    dump()
    result = turtle()
    print(result)


if __name__ == "__main__":
    dgm = test_create_gasmonitordevice()
    co2 = test_create_co2monitordevice()
    co2_temp = test_create_co2monitordevice_with_temperature()
    result = turtle()
    with open("test_device-004_results.ttl", "w") as file:
        file.write(result)
    print("Check file : test_device-004_results.ttl")
    print(result)
    graph = get_datagraph()
